from backend.config import settings
from backend.agents.state import AgentState
from backend.llm_factory import get_llm
import json
import re


class PlannerAgent:
    def __init__(self):
        pass
    
    def plan(self, state: AgentState) -> dict:
        user_query = state['messages'][-1]['content']
        is_deep_think = state.get('deep_think', False)
        llm = get_llm(
            temperature=0.1,
            max_tokens=250,
            deep_think=is_deep_think,
        )

        cot_instruction = (
            "\nIMPORTANT: Think step-by-step. First, analyze the error. "
            "Second, identify the missing information. Third, formulate the task."
            if is_deep_think else ""
        )

        prompt = f"""You are an expert AI Research Planner. 
Your job is to break down the user's query into 1 to 3 actionable sub-tasks.

User Query: "{user_query}"
{cot_instruction}

Assign each task to one of these specialized agents:
- "researcher": For gathering facts, searching logs, or reading runbooks.
- "coder": For writing Python scripts or analyzing data.
- "writer": For summarizing or writing the final report.

Output ONLY a valid JSON object in this exact format:
{{
    "tasks": [
        {{"task": "description of task 1", "agent": "researcher"}}
    ]
}}
Do not include any markdown formatting or extra text. Just the JSON."""

        response = llm.invoke(prompt)
        content = response.content.strip()
        
        try:
            # Try to extract JSON using regex
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                json_str = match.group(0)
                plan_data = json.loads(json_str)
                if "tasks" in plan_data and isinstance(plan_data["tasks"], list):
                    return {
                        "task_plan": plan_data["tasks"],
                        "current_agent": "planner",
                        "trace_log": [{
                            "agent": "Planner",
                            "action": "Parsed query and created task plan",
                            "details": plan_data["tasks"]
                        }]
                    }
            raise ValueError("No valid JSON found")
        except Exception as e:
            print(f"⚠️ [Planner] JSON parsing failed: {e}")
            print(f"📝 Raw LLM output: {content[:150]}...")
            # FALLBACK: assign a default researcher task
            return {
                "task_plan": [{"task": user_query, "agent": "researcher"}],
                "current_agent": "planner",
                "trace_log": [{
                    "agent": "Planner",
                    "action": "Fallback: created default researcher task",
                    "details": user_query
                }]
            }