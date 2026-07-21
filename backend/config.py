from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # App
    APP_NAME: str = "NexusAI"
    DEBUG: bool = True
    ENV: str = "development"

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MAIN_MODEL: str = "qwen2.5:3b"
    OLLAMA_CODER_MODEL: str = "qwen2.5-coder:7b"
    OLLAMA_EMBED_MODEL: str = "nomic-embed-text:latest"
    OLLAMA_FAST_MODEL: str = "qwen2.5:3b"
    OLLAMA_DEEP_MODEL: str = "phi3:3.8b"

    # Cloud API support
    USE_CLOUD_LLM: bool = False
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Groq (Ultra-fast, free tier available)
    # ============ GROQ CLOUD ============
    USE_CLOUD_LLM: bool = False
    GROQ_API_KEY: Optional[str] = None
    GROQ_FAST_MODEL: str = "llama-3.1-8b-instant"      # Blazing fast ~1s
    GROQ_DEEP_MODEL: str = "llama-3.3-70b-versatile"   # Deep reasoning ~3s
    GROQ_MODEL: Optional[str] = None
    # Database
    DATABASE_URL: str = "postgresql://nexusai:password@localhost:5432/nexusai_db"
    POSTGRES_USER: str = "nexusai"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "nexusai_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # MLflow
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    MLFLOW_EXPERIMENT_NAME: str = "nexusai-agents"

    # Arize Phoenix
    PHOENIX_PORT: int = 6006
    PHOENIX_HOST: str = "localhost"

    # MCP
    MCP_SERVER_HOST: str = "localhost"
    MCP_SERVER_PORT: int = 8080

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Frontend & CORS
    FRONTEND_URL: str = "http://localhost:3000"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # External APIs
    TAVILY_API_KEY: Optional[str] = None

    # Vector DB
    EMBEDDING_DIMENSION: int = 768

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get settings instance"""
    return settings