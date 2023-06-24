from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """ Settings class """
    
    app_env: str = Field(..., env="APP_ENV")
    api_prefix: str = Field(..., env="API_PREFIX")
    allowed_hosts: str = Field(..., env="ALLOWED_HOSTS")
    time_zone: str = "UTC"
    api_key:str = Field(..., env="OPENAI_KEY")
    openai_model:str = Field(..., env="OPENAI_MODEL")
    max_retries:int = Field(..., env="MAX_RETRIES")

    class Config:
        """ Config class"""
        env_file = ".env"


settings = Settings()
