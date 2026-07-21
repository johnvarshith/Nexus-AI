from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from backend.config import settings
from backend.agents.state import AgentState

# Initialize Model
llm = ChatOllama(
    model=settings.OLLAMA_MAIN_MODEL, 
    base_url=settings.OLLAMA_BASE_URL, 
    temperature=0.7
)

def agent_node(state: AgentState):
    # LangChain expects messages in a specific format. 
    # We pass the entire history so the LLM has context.
    messages = state['messages']
    
    # Invoke the LLM with the full history
    response = llm.invoke(messages)
    
    # Return the assistant's response to be added to the state
    return {"messages": [{"role": "assistant", "content": response.content}]}

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

app = workflow.compile()