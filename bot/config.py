from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    bot_token: Optional[str] = None
    lms_api_base_url: str = "http://localhost:42002"
    lms_api_key: Optional[str] = None
    llm_api_key: Optional[str] = ""
    llm_api_base_url: Optional[str] = ""
    llm_api_model: str = "coder-model"
    timeout_seconds: int = 5

    class Config:
        env_file = ".env.bot.secret"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
