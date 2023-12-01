from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env" # env file path

settings = Settings()