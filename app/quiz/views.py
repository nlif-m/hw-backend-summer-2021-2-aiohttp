from aiohttp_apispec import (
    json_schema,
    docs,
    response_schema,
    request_schema,
    querystring_schema,
)
from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest

from app.quiz.schemes import (
    ThemeSchema,
    ThemeListSchema,
    QuestionSchema,
    ListQuestionSchema,
    ListQuestionRequestSchema,
)
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


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    async def post(self):
        # TODO: find the way to validate in another place
        title = self.data["title"]
        existed_question = await self.store.quizzes.get_question_by_title(title)
        if existed_question:
            raise HTTPConflict(reason="question already exists")

        theme_id = self.data["theme_id"]
        existed_theme = await self.store.quizzes.get_theme_by_id(theme_id)
        if not existed_theme:
            raise HTTPNotFound(reason="theme not exists")

        amount_of_correct_answers = 0
        answers = self.data["answers"]
        for answer in answers:
            if answer["is_correct"]:
                amount_of_correct_answers += 1
        if amount_of_correct_answers > 1:
            raise HTTPBadRequest(reason="amount of correct answers are greater than 1")
        if amount_of_correct_answers == 0:
            raise HTTPBadRequest(reason="all answers are incorrect")

        question = await self.store.quizzes.create_question(title, theme_id, answers)
        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ListQuestionRequestSchema)
    async def get(self):
        theme_id = self.request.query.get("theme_id")
        if not theme_id:
            questions = await self.store.quizzes.list_questions()
            return json_response(
                data=ListQuestionSchema().dump({"questions": questions})
            )

        theme_id = int(theme_id)
        questions = await self.store.quizzes.list_questions(theme_id)
        return json_response(data=ListQuestionSchema().dump({"questions": questions}))
