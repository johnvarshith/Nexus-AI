from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from backend.agents.state import AgentState
from backend.agents.planner import PlannerAgent
from backend.agents.researcher import researcher_node
from backend.agents.coder import coder_node
from backend.agents.critic import CriticAgent
from backend.agents.clarifier import clarifier_node
from backend.llm_factory import get_llm
from typing import Literal

planner = PlannerAgent()
critic = CriticAgent()

def writer_node(state: AgentState) -> dict:
    print("✍️ [Writer] Generating final Incident Report...")
    llm = get_llm(
        temperature=0.3,
        max_tokens=400,
        deep_think=state.get('deep_think', False),
    )
    
    latest_user_query = ""
    latest_fix = ""
    critic_feedback = ""
    
    for msg in reversed(state.get('messages', [])):
        if msg['role'] == 'user' and not latest_user_query:
            latest_user_query = msg['content']
        if msg['role'] == 'assistant' and "CRITIC FEEDBACK:" in msg['content']:
            critic_feedback = msg['content']
        if msg['role'] == 'assistant' and ("Generated Code:" in msg['content'] or "PROPOSED CODE FIX" in msg['content']):
            latest_fix = msg['content']
            break
    
    fix_status = state.get('fix_status', 'PENDING')
    confidence = state.get('confidence_score', 0)
    recent_context = state.get('messages', [])[-5:]
    prompt = f"""You are an SRE writing a final Incident Report.

    **CRITICAL: Focus ONLY on the MOST RECENT user query.**
    
    Latest User Query: {latest_user_query}
    
    Generated Code/Fix: {latest_fix if latest_fix else 'No fix was generated.'}
    
    Critic's Feedback: {critic_feedback if critic_feedback else 'No feedback provided.'}
    
    Fix Status: {fix_status}
    Confidence Score: {confidence}%
    
    RESEARCH LOGS (for context):
    {recent_context}
    
    **Instructions:**
    - If the fix was APPROVED, write a confident report with the fix steps.
    - If the fix was REJECTED, write a report explaining the rejection, the research findings, and suggest alternative approaches or ask the user for specific logs.
    - Always include Root Cause Analysis, Proposed Fix (or attempted fix), and Prevention Steps.
    - Be honest about what worked and what didn't.
    
    Output a clean, professional Markdown Incident Report."""
    
    response = llm.invoke(prompt)
    return {"messages": [{"role": "assistant", "content": response.content}]}

def route_after_planner(state: AgentState) -> Literal["researcher", "coder", "writer"]:
    task_plan = state.get('task_plan', [])
    if not task_plan:
        print("⚠️ [Router] No task plan found. Routing to writer.")
        return "writer"
    agent = task_plan[0].get('agent', 'researcher')
    if agent not in ['researcher', 'coder', 'writer']:
        agent = 'researcher'
    return agent

def route_after_researcher(state: AgentState) -> Literal["coder", "writer"]:
    task_plan = state.get('task_plan', [])
    if task_plan:
        task_plan.pop(0)
    if not task_plan:
        return "writer"
    agent = task_plan[0].get('agent', 'coder')
    if agent not in ['coder', 'writer']:
        agent = 'coder'
    return agent

def route_after_critic(state: AgentState) -> Literal["writer", "coder", "clarifier"]:
    """
    Routes after Critic:
    - If the Critic explicitly asks for clarification (rare, only for empty inputs), go to Clarifier.
    - If the fix is APPROVED, go to Writer.
    - If the fix is REJECTED, force the Writer to generate a report with the rejection feedback.
    - If retry count exceeds 2, still go to Writer (do NOT ask for clarification).
    """
    status = state.get('fix_status', 'REJECTED')
    needs_clarification = state.get('needs_clarification', False)
    retry_count = state.get('retry_count', 0)
    
    # ONLY go to Clarifier if the critic explicitly asks for it (extremely rare)
    if needs_clarification:
        print(f"🛑 [Router] Explicit clarification requested. Routing to Clarifier.")
        return "clarifier"
    
    # If approved or rejected, go to Writer (forced report generation)
    if status in ["APPROVED", "REJECTED"]:
        if retry_count >= 2:
            print(f"🛑 [Router] Max retries ({retry_count}) reached. Forcing Writer to generate report.")
        else:
            print(f"🔄 [Router] Status: {status}. Routing to Writer (even if rejected).")
        return "writer"
    
    # Fallback: if status is PENDING or unknown, retry with Coder
    print(f"🔄 [Router] Status: {status}. Routing back to Coder (Attempt {retry_count + 1}).")
    return "coder"
# --- BUILD THE GRAPH ---
workflow = StateGraph(AgentState)

workflow.add_node("planner", planner.plan)
workflow.add_node("researcher", researcher_node)
workflow.add_node("coder", coder_node)
workflow.add_node("critic", critic.critique)
workflow.add_node("clarifier", clarifier_node)
workflow.add_node("writer", writer_node)

workflow.set_entry_point("planner")

workflow.add_conditional_edges("planner", route_after_planner, {"researcher": "researcher", "coder": "coder", "writer": "writer"})
workflow.add_conditional_edges("researcher", route_after_researcher, {"coder": "coder", "writer": "writer"})

workflow.add_edge("coder", "critic")
workflow.add_conditional_edges("critic", route_after_critic, {"writer": "writer", "coder": "coder", "clarifier": "clarifier"})

workflow.add_edge("clarifier", END)
workflow.add_edge("writer", END)

memory = InMemorySaver()
app = workflow.compile(checkpointer=memory)