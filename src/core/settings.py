from enum import Enum
from typing import Any
from urllib.parse import quote_plus

from pydantic import BaseSettings, Field, SecretStr, validator


class EnvironmentTypes(Enum):
    test: str = "test"
    local: str = "local"
    dev: str = "dev"
    prod: str = "prod"


class BaseAppSettings(BaseSettings):
    environment: EnvironmentTypes = Field(EnvironmentTypes.prod, env="API_ENVIRONMENT")
    debug: bool = True
    title: str = "Budget service"
    version: str = "0.1.0"
    allowed_hosts: list[str] = ["*"]
    db_driver_name: str = "postgresql+asyncpg"
    db_host: str = Field("budget-pg", env="DATABASE_HOST")
    db_username: str = Field("budget", env="DATABASE_USERNAME")
    db_password: SecretStr = Field("budget", env="DATABASE_PASSWORD")
    db_database: str = Field("budget", env="DATABASE_NAME")
    db_port: int | None

    @property
    def get_db_creds(self):
        return {
            "drivername": self.db_driver_name,
            "username": self.db_username,
            "host": self.db_host,
            "port": self.db_port,
            "database": self.db_database,
            "password": self.db_password.get_secret_value(),
        }

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
        }


class TestSettings(BaseAppSettings):
    title: str = "Test environment - Budget service"


class LocalSettings(BaseAppSettings):
    title: str = "Local environment - Budget service"


class DevelopmentSettings(BaseAppSettings):
    title: str = "Development environment - Budget service"


class ProductionSettings(BaseAppSettings):
    debug: bool = False
