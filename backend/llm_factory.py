from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from backend.config import settings

def get_llm(
    model_name: str = None,
    temperature: float = 0.1,
    max_tokens: int = 300,
    deep_think: bool = False
):
    """
    Returns the appropriate LLM based on USE_CLOUD_LLM flag.
    """
    model_to_use = settings.GROQ_DEEP_MODEL if deep_think else settings.GROQ_FAST_MODEL
    if settings.USE_CLOUD_LLM:
        return ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=model_to_use,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    else:
        if not model_name:
            model_name = settings.OLLAMA_DEEP_MODEL if deep_think else settings.OLLAMA_MAIN_MODEL
        return ChatOllama(
            model=model_name,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=temperature,
            model_kwargs={"num_predict": max_tokens},
        )