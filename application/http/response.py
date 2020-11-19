from enum import Enum
from typing import Dict
from dataclasses import dataclass

from application.utils import get_date_string_utc


# noinspection PyPep8Naming
class HTTP_STATUS(Enum):
    OK = "200 OK"
    NOT_FOUND = "404 Not Found"
    METHOD_NOT_ALLOWED = "405 Method Not Allowed"
    SERVER_ERROR = "500 Internal Server Error"


@dataclass
class Response:
    status: HTTP_STATUS = HTTP_STATUS.OK
    headers: Dict[str, str] = None
    cookies: Dict[str, str] = None
    body: bytes = b""
    content_type: str = None

    def __post_init__(self):
        if self.headers is None:
            self.headers = {
                "Content-type": "application/octet-stream",
                "Date": get_date_string_utc(),
                "Server": "HenaDjango",
                "Connection": "close",
            }

        if self.content_type is not None:
            self.headers["Content-type"] = self.content_type

    def set_cookie(self, key: str, value=""):
        if self.cookies is None:
            self.cookies = {}
        self.cookies[key] = value


class ResponseNotFound(Response):
    status = HTTP_STATUS.NOT_FOUND


class ResponseServerError(Response):
    status = HTTP_STATUS.SERVER_ERROR
