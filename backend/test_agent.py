from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from typing import TypedDict

# Initialize model
llm = ChatOllama(model="qwen2.5:7b", temperature=0)

# Simple state
class AgentState(TypedDict):
    messages: list

# Simple agent
def agent_node(state: AgentState):
    response = llm.invoke(state['messages'][-1])
    return {"messages": [response.content]}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
app = workflow.compile()

# Test it
if __name__ == "__main__":
    result = app.invoke({"messages": ["What is AI?"]})
    print(result['messages'][0])