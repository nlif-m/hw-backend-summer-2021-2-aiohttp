import random
import typing
from typing import Optional

from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message
from app.store.vk_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.key: Optional[str] = None
        self.server: Optional[str] = None
        self.poller: Optional[Poller] = None
        self.ts: Optional[int] = None

    async def connect(self, app: "Application"):
        self.session = ClientSession()
        await self._get_long_poll_service()
        self.poller = Poller(self.app.store)
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        await self.session.close()
        await self.poller.stop()

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        url = host + method + "?"
        if "v" not in params:
            params["v"] = "5.131"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def _get_long_poll_service(self):
        url = self._build_query(
            host="https://api.vk.com/method",
            method="/groups.getLongPollServer",
            params={
                "group_id": self.app.config.bot.group_id,
                "access_token": self.app.config.bot.token,
            },
        )

        async with self.session.get(url) as resp:
            data = (await resp.json())["response"]
            self.app.logger.info(data)
            self.ts = data["ts"]
            self.server = data["server"]
            self.key = data["key"]

    async def poll(self) -> dict:
        self.app.logger.info("new poll request")
        url = f"{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25"
        self.app.logger.info(f"long poll with {url}")
        async with self.session.get(url) as resp:
            data = await resp.json()
            self.app.logger.info(f"poll:{data}")
            self.ts = data["ts"]
            return data["updates"]

    async def send_message(self, message: Message) -> None:
        url = self._build_query(
            host="https://api.vk.com/method",
            method="/messages.send",
            params={
                "peer_id": message.user_id,
                "message": message.text,
                "access_token": self.app.config.bot.token,
                "random_id": random.randint(0, 10000000),
            },
        )
        async with self.session.get(url) as resp:
            data = await resp.json()
            self.app.logger.info(data)
