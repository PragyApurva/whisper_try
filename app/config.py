# app/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    whisper_model_size: str = "base"
    ollama_host: str = "http://localhost:11434"

    class Config:
        env_file = ".env"

settings = Settings()