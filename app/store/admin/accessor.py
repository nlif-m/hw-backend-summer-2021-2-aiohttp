import typing
from hashlib import sha256
from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        self.app.database.admins.append(await self.create_admin(
            self.app.config.admin.email,
            self.app.config.admin.password
        ))

    async def get_by_email(self, email: str) -> Optional[Admin]:
        admins: list[Admin] = self.app.database.admins
        for admin in admins:
            if admin.email == email:
                return admin
        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        return Admin(self.app.database.next_admin_id,
                     email=email,
                     password=sha256(password.encode()).hexdigest())
