from marshmallow import Schema, fields

from app.web.schemes import OkResponseSchema


class AccountSchema(Schema):
    user_id = fields.Int()
    game_id = fields.Int()
    vote = fields.Bool()
    scores = fields.Int()
    photo_num = fields.Str()


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    profile_photo_id = fields.Str()
    wins = fields.Int()
    total_games = fields.Int()
    efficiency = fields.Float()


class GameRequestSchema(Schema):
    chat_id = fields.Int(required=True)


class GameSchema(GameRequestSchema):
    bot_state = fields.Str()
    current_round = fields.Int()
    players = fields.Nested(UserSchema, many=True)
    accounts = fields.Nested(AccountSchema, many=True)


class GameResponseSchema(OkResponseSchema):
    data = fields.Nested(GameSchema)
