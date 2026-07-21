from langchain_ollama import ChatOllama
from backend.config import settings
from backend.agents.state import AgentState
import importlib
import json
import re


def get_llm(model_name=None, temperature=0.1):
    """Factory to switch between Ollama and Cloud APIs."""
    if settings.USE_CLOUD_LLM:
        try:
            chat_openai = importlib.import_module("langchain_openai")
            ChatOpenAI = chat_openai.ChatOpenAI
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise ImportError("The 'langchain-openai' package is required when USE_CLOUD_LLM is enabled.") from exc

        return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            temperature=temperature,
            max_tokens=300,
        )

    return ChatOllama(
        model=model_name or settings.OLLAMA_MAIN_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=temperature,
        model_kwargs={"num_predict": 150},
    )


class PlannerAgent:
    def __init__(self):
        self.llm = get_llm(settings.OLLAMA_MAIN_MODEL, 0.1)
    
    def plan(self, state: AgentState) -> dict:
        user_query = state['messages'][-1]['content']
        is_deep_think = state.get('deep_think', False)
        
        model_to_use = settings.OLLAMA_DEEP_MODEL if is_deep_think else settings.OLLAMA_MAIN_MODEL
        if model_to_use != self.llm.model:
            self.llm = ChatOllama(
                model=model_to_use,
                base_url=settings.OLLAMA_BASE_URL,
                temperature=0.1,
                model_kwargs={"num_predict": 150}
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

        response = self.llm.invoke(prompt)
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