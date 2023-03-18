from typing import Optional, TYPE_CHECKING, List

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from sqlalchemy.sql import Select, Insert, Update, Delete

if TYPE_CHECKING:
    from app.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        self._app = app
        self._engine: Optional[AsyncEngine] = None
        self.session: Optional[async_sessionmaker] = None
        self._database_url = self.generate_pg_database_url()

    async def connect(self, *_: list, **__: dict) -> None:
        self._engine = create_async_engine(self._database_url, future=True)
        self.session = async_sessionmaker(bind=self._engine, expire_on_commit=False)

        await self._app.store.admins.create_admin(email=self._app.config.admin.email,
                                                  password=self._app.config.admin.password)

    async def disconnect(self, *_: list, **__: dict) -> None:
        self.session = None

        if self._engine:
            await self._engine.dispose()
            self._engine = None

    async def execute_statement(self, statement: Select | Insert | Update | Delete) -> None:
        async with self.session() as session:
            await session.execute(statement)
            await session.commit()
        await self._engine.dispose()

    async def execute_statement_scalars(self, statement: Select | Insert | Update | Delete) -> List:
        async with self.session() as session:
            scalars = await session.scalars(statement)
            await session.commit()
        await self._engine.dispose()
        return scalars.all()

    def generate_pg_database_url(self) -> str:
        return "{driver}://{user}:{password}@{host}/{db_name}".format(
            driver=self._app.config.database.driver,
            user=self._app.config.database.user,
            password=self._app.config.database.password,
            host=self._app.config.database.host,
            db_name=self._app.config.database.database,
        )
