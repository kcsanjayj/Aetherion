"""
Secure settings module - uses environment variables only
No hardcoded secrets, no .env files in repo
"""
import os
import logging

logger = logging.getLogger(__name__)


class Settings:
    """Centralized settings using environment variables only"""
    
    # AI Provider API Keys (loaded from env, never hardcoded)
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY", "")
    
    # Optional configs with defaults (DEBUG off by default for security)
    DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    
    # Server config
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", "8000"))
    
    # Vector DB
    CHROMA_DB_PATH = os.environ.get("CHROMA_DB_PATH", "./data/chroma_db")
    
    @staticmethod
    def get_api_key(provider: str) -> str:
        """Get API key for a provider - returns empty string if not set"""
        key_map = {
            "gemini": Settings.GOOGLE_API_KEY,
            "google": Settings.GOOGLE_API_KEY,
            "openai": Settings.OPENAI_API_KEY,
            "anthropic": Settings.ANTHROPIC_API_KEY,
            "claude": Settings.ANTHROPIC_API_KEY,
            "nvidia": Settings.NVIDIA_API_KEY,
            "groq": Settings.GROQ_API_KEY,
            "huggingface": Settings.HUGGINGFACE_API_KEY,
            "hf": Settings.HUGGINGFACE_API_KEY,
        }
        return key_map.get(provider.lower(), "")
    
    @staticmethod
    def validate_required_keys():
        """Check configured AI providers - optional as users provide their own keys"""
        keys = [
            Settings.GOOGLE_API_KEY,
            Settings.OPENAI_API_KEY,
            Settings.ANTHROPIC_API_KEY,
            Settings.NVIDIA_API_KEY,
            Settings.GROQ_API_KEY,
            Settings.HUGGINGFACE_API_KEY,
        ]
        
        configured = []
        if Settings.GOOGLE_API_KEY:
            configured.append("Google/Gemini")
        if Settings.OPENAI_API_KEY:
            configured.append("OpenAI")
        if Settings.ANTHROPIC_API_KEY:
            configured.append("Anthropic")
        if Settings.NVIDIA_API_KEY:
            configured.append("NVIDIA")
        if Settings.GROQ_API_KEY:
            configured.append("Groq")
        if Settings.HUGGINGFACE_API_KEY:
            configured.append("HuggingFace")
        
        if configured:
            logger.info(f"Server-configured AI providers: {', '.join(configured)}")
        else:
            logger.info("No server-configured AI providers. Users must provide their own API keys.")
        
        return True


# Validate on module import
Settings.validate_required_keys()
