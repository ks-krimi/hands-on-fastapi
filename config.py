from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    algorithm: str
    access_token_expire_minutes: int
    secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
