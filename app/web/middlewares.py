import json
import typing

from aiohttp.web_exceptions import (
    HTTPUnprocessableEntity,
    HTTPForbidden,
    HTTPMethodNotAllowed,
    HTTPUnauthorized,
    HTTPConflict,
    HTTPNotFound,
    HTTPBadRequest
)
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import get_session

from app.admin.models import Admin
from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request


@middleware
async def auth_middleware(request: "Request", handler: callable):
    session = await get_session(request)
    if session:
        request.admin = Admin.from_session(session)
    return await handler(request)


HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler: callable):
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPBadRequest:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message="Request data is incorrect. Please check and try again",
        )
    except HTTPUnauthorized:
        return error_json_response(
            http_status=401,
            status=HTTP_ERROR_CODES[401],
            message="Please login to get access to this data",
        )
    except HTTPForbidden:
        return error_json_response(
            http_status=403,
            status=HTTP_ERROR_CODES[403],
            message="Login data is incorrect. Please check and try again",
        )
    except HTTPNotFound:
        return error_json_response(
            http_status=404,
            status=HTTP_ERROR_CODES[404],
            message="Request data is not found. Please check and try again",
        )
    except HTTPMethodNotAllowed:
        return error_json_response(
            http_status=405,
            status=HTTP_ERROR_CODES[405],
            message="This request method is not allowed",
        )
    except HTTPConflict:
        return error_json_response(
            http_status=409,
            status=HTTP_ERROR_CODES[409],
            message="The data conflict appeared during request",
        )
    except Exception as e:
        return error_json_response(
            http_status=500, status="internal server error", message=str(e)
        )


def setup_middlewares(app: "Application"):
    app.middlewares.append(auth_middleware)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
