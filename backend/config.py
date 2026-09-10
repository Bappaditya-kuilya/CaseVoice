from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RIME_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    DATABASE_PATH: str = "./casevoice.db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
