from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.quiz.models import Theme, Question, Answer


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = Theme(id=self.app.database.next_theme_id, title=str(title))
        self.app.database.themes.append(theme)
        return theme

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        for theme in self.app.database.themes:
            if title == theme.title:
                return theme
            return None

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        for theme in self.app.database.themes:
            if id_ == theme.id:
                return theme
            return None

    async def list_themes(self) -> list[Theme]:
        return self.app.database.themes

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        for question in self.app.database.questions:
            if title == question.title:
                return question
        return None

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        # TODO: Add a validation to answers
        question = Question(
            self.app.database.next_question_id, title, theme_id, answers
        )
        self.app.database.questions.append(question)
        return question

    async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:
        if not theme_id:
            return self.app.database.questions

        filtered_questions: list[Question] = []

        for question in self.app.database.questions:
            if theme_id == question.theme_id:
                filtered_questions.append(question)

        return filtered_questions
