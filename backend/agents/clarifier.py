from backend.agents.state import AgentState

def clarifier_node(state: AgentState) -> dict:
    """Pauses the graph and sends a clarification question to the user."""
    question = state.get('clarification_question', 'Can you provide more details?')
    
    print(f"🙋 [Clarifier] Asking user: '{question}'")
    
    # We return a special message that the frontend will render as a "Question Bubble"
    return {
        "messages": [{
            "role": "assistant", 
            "content": f"🛑 CLARIFICATION NEEDED: {question}"
        }],
        "needs_clarification": False, # Reset the flag
        "fix_status": "PENDING_USER_INPUT"
    }