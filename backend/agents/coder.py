from backend.agents.state import AgentState
from backend.llm_factory import get_llm
import sys
from io import StringIO

class CoderAgent:
    def __init__(self):
        pass
    
    def extract_python_code(self, text: str) -> str:
        if "```python" in text:
            try:
                return text.split("```python")[1].split("```")[0].strip()
            except IndexError:
                pass
        if "```" in text:
            try:
                return text.split("```")[1].split("```")[0].strip()
            except IndexError:
                pass
        return text.strip()
    
    def safe_execute_python(self, code: str) -> str:
        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output
        try:
            exec(code, {"__builtins__": __builtins__})
            result = redirected_output.getvalue()
            return result if result else "Code executed successfully (no output)."
        except Exception as e:
            return f"Execution Error: {str(e)}"
        finally:
            sys.stdout = old_stdout
    
    def coder_node(self, state: AgentState) -> dict:
        # Get current retry count or default to 0, then increment
        current_retries = state.get('retry_count', 0) + 1
        
        current_task = state['task_plan'][0]['task'] if state.get('task_plan') else "Fix the issue"
        original_error = state['messages'][0]['content'] if state.get('messages') else "No error provided."
        research_findings = "No research findings."
        critic_feedback = "No critic feedback."
        
        for msg in state.get('messages', []):
            content = msg['content']
            if "SYSTEM LOGS:" in content or "HISTORICAL RUNBOOK" in content:
                research_findings = content
            if "CRITIC FEEDBACK:" in content:
                critic_feedback = content
        
        print(f"🔧 [Coder] Task: '{current_task}' (Attempt {current_retries})")
        if critic_feedback != "No critic feedback.":
            print("⚠️ [Coder] Incorporating critic feedback...")
        
        prompt = f"""You are an expert SRE and Python developer fixing a production incident.

ORIGINAL INCIDENT REPORT:
{original_error}

RESEARCH FINDINGS (Logs / Runbooks):
{research_findings}

PREVIOUS ATTEMPT FEEDBACK (Critic):
{critic_feedback}

YOUR TASK:
{current_task}

Write a Python script that:
1. Demonstrates the fix for the issue.
2. Includes proper error handling.
3. Is production-ready.

Output ONLY the Python code. Do not include explanations or markdown formatting."""

        print("⏳ [Coder] Generating code...")
        llm = get_llm(temperature=0.2, max_tokens=300)
        response = llm.invoke(prompt)
        code = self.extract_python_code(response.content)
        
        print("⚙️ [Coder] Executing generated code...")
        execution_result = self.safe_execute_python(code)
        
        observation = f"Generated Code:\n```python\n{code}\n```\n\nExecution Result:\n{execution_result}"
        print("✅ [Coder] Code execution complete.")
        
        return {
            "messages": [{"role": "assistant", "content": observation}],
            "current_agent": "coder",
            "retry_count": current_retries,   # 👈 Incremented correctly
            "trace_log": [{"agent": "Coder", "action": f"Generated and executed code (Attempt {current_retries})", "details": code[:100]}]
        }

coder_agent = CoderAgent()
coder_node = coder_agent.coder_node