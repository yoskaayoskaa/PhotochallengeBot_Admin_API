import typing

from aiohttp.web_exceptions import HTTPUnauthorized

if typing.TYPE_CHECKING:
    from app.web.app import Request


class AuthRequiredMixin:
    @staticmethod
    def login_required(request: "Request") -> None:
        if not getattr(request, "admin", None):
            raise HTTPUnauthorized
