import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

ENV: str = ""

class Configs(BaseSettings):

    ENV: str = os.getenv("ENV", "dev")
    API_V1_STR: str = "/api/v1"
    API_V2_STR: str = "/api/v2"

    APP_NAME: str = "GDX APPLICATION"
    APP_VERSION: str = "1.0.0"

    DB_ENGINE_MAPPER: dict = {
        "postgresql" : "postgresql",
    }

    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"
    
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # auth
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: str = os.getenv("JWT_ACCESS_TOKEN_EXPIRATION")  # 60 minutes * 24 hours * 30 days = 30 days


    # database
    DB: str = os.getenv("DB")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")

    POSTGRES_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB}"

    class Config:
            case_sensitive = True


class TestConfigs(Configs):
    ENV: str = "test"

configs = Configs()


if ENV == "prod":
    pass
elif ENV == "stage":
    pass
elif ENV == "test":
    setting = TestConfigs()