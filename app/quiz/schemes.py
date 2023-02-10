from marshmallow import Schema, fields
from marshmallow.validate import Length


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)


class QuestionSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested(
        AnswerSchema, required=True, many=True, validate=Length(min=2)
    )


class ThemeListSchema(Schema):
    themes = fields.Nested(ThemeSchema, many=True)


class ListQuestionRequestSchema(Schema):
    theme_id = fields.Int(allow_none=True)


class ListQuestionSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True)
