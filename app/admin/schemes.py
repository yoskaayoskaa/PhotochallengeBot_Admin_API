from marshmallow import Schema, fields

from app.web.schemes import OkResponseSchema


class AdminSchema(Schema):
    id = fields.Int()
    email = fields.Str()


class AdminLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class AdminResponseSchema(OkResponseSchema):
    data = fields.Nested(AdminSchema)
