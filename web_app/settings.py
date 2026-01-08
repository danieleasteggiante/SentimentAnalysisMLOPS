from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    DURATION_MINUTES: int

    SMTP_SERVER : str
    SMTP_PORT : str
    SENDER_EMAIL : str
    PASSWORD_EMAIL : str

    BASE_URL : str
    DATABASE_URL : str

    PROTECTED_ROUTES : list[str]

    class Config:
        env_file = ".env"



settings = Settings()