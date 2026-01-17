from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    FRONTEND_URL: str = "http://localhost:3000"
    APP_NAME: str
    DEBUG: bool = False

    DATABASE_URL: str

    JWT_ACCESS_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
