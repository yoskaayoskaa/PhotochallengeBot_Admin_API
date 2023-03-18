import typing

from app.game.views import WholeGameView

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    app.router.add_view("/game.whole_game", WholeGameView)
