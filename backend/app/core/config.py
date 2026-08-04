from functools import lru_cache
from pathlib import Path

import yaml
from pydantic_settings import BaseSettings

# This finds the .env file in the project root
# no matter where you run the command from
ENV_FILE_PATH = Path(__file__).parent.parent.parent.parent / ".env"


class Settings(BaseSettings):
    # App
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "changeme"

    # LLM APIs (optional, fallback only)
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # Ollama (primary - open source local models)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"
    ollama_embed_model: str = "nomic-embed-text"

    # Database
    database_url: str = ""
    postgres_user: str = "nutriagent"
    postgres_password: str = "nutriagent"
    postgres_db: str = "nutriagent"

    model_config = {
        "env_file": str(ENV_FILE_PATH),
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def get_yaml_config() -> dict:
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


settings = get_settings()
yaml_config = get_yaml_config()
