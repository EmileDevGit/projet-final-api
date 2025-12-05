from pydantic_settings import BaseSettings, SettingsConfigDict
import os

ENV = os.getenv("ENV", "development")
if ENV == "test":
    env_file = ".env.test"
else:
    env_file = ".env"


class Settings(BaseSettings):

    DATABASE_HOST: str = "sapienta_db"
    DATABASE_URL: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_ENDPOINT: str = "http://sapienta_auth:8080/token"
    TOKEN_VALIDATE_ENDPOINT: str = "http://sapienta_auth:8080/token/validate"
    TOKEN_REFRESH_ENDPOINT: str = "http://sapienta_auth:8080/token/refresh"

    model_config = SettingsConfigDict(
        extra="ignore", env_file=env_file, env_file_encoding="utf-8")


settings = Settings()
