from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.base.base_accessor import BaseAccessor
from app.game.models import Game, GameModel, AccountModel


class GameAccessor(BaseAccessor):
    async def get_game_dataclass(self, chat_id: int) -> Optional[Game]:
        statement_game = select(GameModel).where(GameModel.chat_id == chat_id).options(selectinload(GameModel.players))
        game_models_list = await self.app.database.execute_statement_scalars(statement=statement_game)

        statement_account = select(AccountModel).where(AccountModel.game_id == chat_id)
        account_models_list = await self.app.database.execute_statement_scalars(statement=statement_account)
        accounts = [account_model.dataclass for account_model in account_models_list]

        return game_models_list[0].transform_to_dataclass(accounts=accounts) if game_models_list else None
