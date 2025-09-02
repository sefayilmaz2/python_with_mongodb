from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database Configuration
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "python_web_api"
    
    # JWT Configuration
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application Configuration
    debug: bool = True
    api_v1_str: str = "/api/v1"
    project_name: str = "Python Web API with MongoDB"
    
    # CORS Configuration
    backend_cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"


settings = Settings()