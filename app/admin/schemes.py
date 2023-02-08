from marshmallow import Schema, fields


class AdminLoginRequestSchema(Schema):
    # TODO: can't use fields.Email because of tests
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AdminLoginResponseSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Str(required=True)
