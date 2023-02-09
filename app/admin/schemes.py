from marshmallow import Schema, fields


class AdminLoginRequestSchema(Schema):
    # TODO: can't use fields.Email because of tests
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AdminSchema(Schema):
    id = fields.Integer(required=True)
    email = fields.Str(required=True)


class AdminLoginResponseSchema(AdminSchema):
    pass


class AdminCurrentResponseSchema(AdminLoginResponseSchema):
    pass
