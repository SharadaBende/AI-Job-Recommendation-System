from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:password@localhost:5432/jobrec"
    adzuna_app_id: str = ""
    adzuna_app_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()