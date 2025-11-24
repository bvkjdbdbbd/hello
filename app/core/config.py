
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    SECRET_KEY: str 

    DATABASE_URL: str

    MAX_FAIL_AUTH: int = 5 

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()