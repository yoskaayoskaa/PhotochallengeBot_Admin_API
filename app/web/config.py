import os
import typing
from dataclasses import dataclass
from dotenv import load_dotenv

if typing.TYPE_CHECKING:
    from app.web.app import Application

load_dotenv()


@dataclass
class SessionConfig:
    key: str


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: str = "5432"
    user: str = "postgres"
    password: str = "postgres"
    database: str = "project"
    driver: str = "postgresql+asyncpg"


@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig = None
    database: DatabaseConfig = None


def setup_config(app: "Application"):
    app.config = Config(
        session=SessionConfig(
            key=str(os.getenv("SESSION_KEY")),
        ),
        admin=AdminConfig(
            email=str(os.getenv("ADMIN_EMAIL")),
            password=str(os.getenv("ADMIN_PASSWORD")),
        ),
        database=DatabaseConfig(
            host=str(os.getenv("PG_HOST")),
            port=str(os.getenv("PG_PORT")),
            user=str(os.getenv("PG_USER")),
            password=str(os.getenv("PG_PASSWORD")),
            database=str(os.getenv("PG_DATABASE")),
            driver=str(os.getenv("PG_DRIVER")),
        ),
    )
