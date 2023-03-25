import os

from dotenv import load_dotenv
from pydantic import PostgresDsn

dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class AppSettings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "App")

    PROJECT_HOST = os.getenv("PROJECT_HOST", "127.0.0.1")
    PROJECT_PORT = int(os.getenv("PROJECT_PORT", 8080))

    SHORT_LINK_LENGTH = int(os.getenv("SHORT_LINK_LENGTH", 6))

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    POSTGRES_DB_TEST: str = os.getenv("POSTGRES_DB_TEST", "postgres_test")
    DATABASE_DSN: PostgresDsn = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    DATABASE_TEST_DSN: PostgresDsn = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB_TEST}"
    )


app_settings = AppSettings()
