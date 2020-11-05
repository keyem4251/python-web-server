from enum import Enum

from application.utils import get_date_string_utc


# noinspection PyPep8Naming
class HTTP_STATUS(Enum):
    OK = "200 OK"
    NOT_FOUND = "404 Not Found."
    SERVER_ERROR = "500 Internal Server Error"


class Response:
    status: HTTP_STATUS
    headers: dict
    body: bytes

    def __init__(self, status: str, body: bytes, headers=None, content_type=None):
        self.status = status
        self.body = body

        if headers:
            self.headers = headers
        else:
            self.headers = {
                "Content-type": "application/octet-stream",
                "Date": get_date_string_utc(),
                "Server": "HenaDjango",
                "Connection": "close",
            }

        if content_type:
            self.headers["Content-type"] = content_type
