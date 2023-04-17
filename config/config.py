from pydantic import BaseSettings, HttpUrl


class SettingsLocal(BaseSettings):
    app_env = "local"

    # DB
    database_url: str
    db_echo = True

    # Auth
    # to get a string like this run:
    # openssl rand -hex 32
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 50

    # Google
    google_api_key: str

    class Config:
        env_file = "config/.env"


settings = SettingsLocal()
