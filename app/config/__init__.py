import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(verbose=True)


class CommonSettings(BaseSettings):
    APP_NAME: str = "VORIAN JOBS API"
    DEBUG_MODE: bool = os.getenv('DEBUG_MODE')


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv('SERVICE_PORT'))


class Settings(CommonSettings, ServerSettings):
    pass


settings = Settings()
