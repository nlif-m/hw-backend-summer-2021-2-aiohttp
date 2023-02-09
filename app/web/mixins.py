from typing import TYPE_CHECKING
from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp.web_response import StreamResponse

if TYPE_CHECKING:
    from app.web.app import Request

    # https://t.me/c/1591931077/10848


class AuthRequiredMixin:
    async def _iter(self) -> StreamResponse:
        if not self.request.admin:
            raise HTTPUnauthorized
        return await super()._iter()
