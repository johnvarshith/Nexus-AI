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
        max_tokens=300,
        deep_think=state.get('deep_think', False),
    )
    
    context = "\n\n".join([msg['content'] for msg in state['messages']])
    prompt = f"""You are an SRE writing a final Incident Report. 
    Confidence Score: {state.get('confidence_score', 0)}%
    
    Context:
    {context}
    
    Output a clean, professional Markdown Incident Report with sections: 
    1. Root Cause Analysis
    2. Proposed Fix
    3. Prevention Steps"""
    
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
    status = state.get('fix_status', 'REJECTED')
    confidence = state.get('confidence_score', 0)
    needs_clarification = state.get('needs_clarification', False)
    retry_count = state.get('retry_count', 0)
    
    # If clarification is needed, go to clarifier immediately
    if needs_clarification:
        return "clarifier"
    
    if status == "APPROVED" and confidence >= 85:
        print(f"✅ [Router] Approved with {confidence}%. Routing to Writer.")
        return "writer"
    
    if retry_count >= 2:
        print(f"🛑 [Router] Max retries ({retry_count}) reached. Routing to Clarifier.")
        return "clarifier"
    
    print(f"🔄 [Router] Rejected. Routing back to Coder (Attempt {retry_count + 1}).")
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