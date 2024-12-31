from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PubSubSettings(BaseModel):
    project_id: str = "local0"
    input_topic: str = "async-worker-in"
    output_topic: str = "async-worker-out"
    max_messages: int = 30


class Settings(BaseSettings):
    pubsub: PubSubSettings = PubSubSettings()
    enabled: bool = True
    port: int = 8000

    model_config = SettingsConfigDict(env_prefix="WORKER", env_nested_delimiter="__")


@lru_cache
def get_settings() -> Settings:
    return Settings()
