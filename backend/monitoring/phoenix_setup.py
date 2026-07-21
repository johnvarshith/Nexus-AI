import phoenix as px
from backend.config import settings

def setup_phoenix():
    """Initialize Arize Phoenix for LLM observability"""
    session = px.launch_app(
        port=settings.PHOENIX_PORT,
        collect=True
    )
    print(f"✅ Phoenix observability running at http://localhost:{settings.PHOENIX_PORT}")
    return session

def instrument_llm_calls():
    """Instrument LangChain calls for Phoenix"""
    from langchain.callbacks import PhoenixCallbackHandler
    
    phoenix_handler = PhoenixCallbackHandler(
        endpoint=f"http://localhost:{settings.PHOENIX_PORT}"
    )
    
    return phoenix_handler