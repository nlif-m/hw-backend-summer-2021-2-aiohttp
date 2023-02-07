from typing import Any, Optional

from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response


def json_response(data: Any = None, status: str = "ok") -> Response:
    if data is None:
        data = {}
    return aiohttp_json_response(
        data={
            "status": status,
            "data": data,
        }
    )


def error_json_response(
    http_status: int,
    status: str = "error",
    message: Optional[str] = None,
    data: Optional[dict] = None,
):
    if message is None:
        message = ""
    if data is None:
        data = {}
    # TODO: Handle key error when accesing HTTP_ERROR_CODES dict
    return aiohttp_json_response(data={"status": status,
                                       "message": message,
                                       "data": data},
                                 status=http_status)
