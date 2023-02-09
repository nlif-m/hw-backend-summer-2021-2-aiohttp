import typing
from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin
from app.web.utils import hash_password

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        self.app.database.admins.append(
            await self.create_admin(
                self.app.config.admin.email, self.app.config.admin.password
            )
        )

    async def get_by_email(self, email: str) -> Optional[Admin]:
        for admin in self.app.database.admins:
            if admin.email == email:
                return admin
        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        return Admin(
            self.app.database.next_admin_id,
            email=email,
            password=hash_password(password),
        )
