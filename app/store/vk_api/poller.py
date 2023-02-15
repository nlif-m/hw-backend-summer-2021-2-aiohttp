from asyncio import Task, create_task, wait
from typing import Optional

from aiohttp.client_exceptions import ClientOSError

from app.store.vk_api.dataclasses import Update, UpdateObject, UpdateMessage
from app.store import Store


class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        self.is_running = True
        self.poll_task = create_task(self.poll())

    async def stop(self):
        self.is_running = False
        if self.poll_task:
            await wait([self.poll_task], timeout=30)

    async def poll(self):
        while self.is_running:
            try:
                raw_updates = await self.store.vk_api.poll()
            except ClientOSError:
                continue
            updates = [
                Update(
                    type=raw_update["type"],
                    object=UpdateObject(
                        UpdateMessage(
                            raw_update["object"]["message"]["from_id"],
                            raw_update["object"]["message"]["text"],
                            raw_update["object"]["message"]["id"],
                        )
                    ),
                )
                for raw_update in raw_updates
            ]
            await self.store.bots_manager.handle_updates(updates)
