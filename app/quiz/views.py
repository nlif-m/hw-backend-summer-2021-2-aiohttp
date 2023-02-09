from aiohttp_apispec import json_schema, docs, response_schema, request_schema
from aiohttp.web_exceptions import HTTPConflict

from app.quiz.schemes import ThemeSchema, ThemeListSchema
from app.web.app import View
from app.web.utils import json_response
from app.web.mixins import AuthRequiredMixin


class ThemeAddView(AuthRequiredMixin, View):
    @response_schema(ThemeSchema)
    @request_schema(ThemeSchema)
    async def post(self):
        title = self.data["title"]
        existed_theme = await self.store.quizzes.get_theme_by_title(title)
        if existed_theme is not None:
            raise HTTPConflict(reason="theme already exists")
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))


class QuestionAddView(View):
    async def post(self):
        raise NotImplementedError


class QuestionListView(View):
    async def get(self):
        raise NotImplementedError
