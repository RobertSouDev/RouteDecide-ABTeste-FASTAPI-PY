"""Configurações centralizadas da aplicação."""
from typing import List


class Settings:
    """Configurações da aplicação."""
    
    # API
    API_TITLE: str = "A/B Testing Backend MVP"
    API_VERSION: str = "0.1.0"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]


settings = Settings()

