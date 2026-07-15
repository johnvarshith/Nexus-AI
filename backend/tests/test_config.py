import pytest
from backend.config import settings, get_settings

def test_settings_loaded():
    """Test that settings are loaded correctly"""
    assert settings.APP_NAME == "NexusAI"
    assert settings.OLLAMA_BASE_URL == "http://localhost:11434"
    assert settings.DEBUG is True

def test_get_settings():
    """Test get_settings function"""
    settings_instance = get_settings()
    assert isinstance(settings_instance, type(settings))