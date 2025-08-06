from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TITLE: str = "CBW Prueba Técnica"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API para la prueba técnica de CBW"
    ENVIRONMENT: str = "dev"
    DEBUGGER: bool = False
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "cbw_db"


settings = Settings()
