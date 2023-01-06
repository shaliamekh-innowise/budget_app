from fastapi import Depends

from adapters.orm_engines.sql_alchemy import SQLAlchemy
from core.config import get_settings
from core.settings import BaseAppSettings


class SQLAlchemyDependency:
    def __init__(self):
        self.sqlalchemy = None

    async def __call__(self, settings: BaseAppSettings = Depends(get_settings)) -> SQLAlchemy:
        self.sqlalchemy = SQLAlchemy.start(settings.get_db_creds()) if not self.sqlalchemy else self.sqlalchemy
        return self.sqlalchemy


get_sql_alchemy = SQLAlchemyDependency()


async def get_db(sqlalchemy: SQLAlchemy = Depends(get_sql_alchemy)):
    async with sqlalchemy.session_maker() as session:
        yield session
