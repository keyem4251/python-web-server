from enum import Enum


# noinspection PyPep8Naming
class HTTP_STATUS(Enum):
    OK = "200 OK"
    NOT_FOUND = "404 Not Found."
    SERVER_ERROR = "500 Internal Server Error"


class Response:
    status: HTTP_STATUS
    headers: dict
    body: bytes

    def __init__(self, status: str, body: bytes, headers: dict):
        self.status = status
        self.headers = headers
        self.body = body
