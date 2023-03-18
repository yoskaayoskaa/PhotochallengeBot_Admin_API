from typing import Optional

from sqlalchemy import select, insert

from app.admin.models import AdminModel, Admin
from app.base.base_accessor import BaseAccessor
from app.web.utils import hash_password


class AdminAccessor(BaseAccessor):
    async def get_by_email(self, email: str) -> Optional[Admin]:
        statement = select(AdminModel).where(AdminModel.email == str(email))
        admin_models_list = await self.app.database.execute_statement_scalars(statement=statement)

        return admin_models_list[0].dataclass if admin_models_list else None

    async def create_admin(self, email: str, password: str) -> None:
        if await self.get_by_email(email=email) is None:
            statement = insert(AdminModel).values(email=email, password=hash_password(password))
            await self.app.database.execute_statement(statement=statement)
