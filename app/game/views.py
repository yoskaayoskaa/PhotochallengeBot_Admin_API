from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import response_schema, docs, request_schema
from app.game.schemes import GameResponseSchema, GameSchema, GameRequestSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class WholeGameView(AuthRequiredMixin, View):
    @docs(tags=["Game"],
          summary="The whole Game information",
          description="Get the current Game information by chat id")
    @request_schema(GameRequestSchema)
    @response_schema(GameResponseSchema, 200)
    async def post(self):
        self.login_required(request=self.request)

        chat_id = self.data["chat_id"]
        game = await self.store.game.get_game_dataclass(chat_id=chat_id)  # Game | None

        if game is None:
            raise HTTPNotFound

        return json_response(data=GameSchema().dump(game))
