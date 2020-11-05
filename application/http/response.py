import datetime
from enum import Enum
from typing import List


# noinspection PyPep8Naming
class HTTP_STATUS(Enum):
    OK = "200 OK"
    NOT_FOUND = "404 Not Found."
    SERVER_ERROR = "500 Internal Server Error"


class Response:
    status: HTTP_STATUS
    headers: List
    body: bytes

    def __init__(self, status: str, body: bytes, headers=None, content_type=None):
        self.status = status
        self.body = body

        if headers:
            self.headers = headers
        else:
            self.headers = [
                ('Content-type', "application/octet-stream"),
                ("Date", self.get_date_string_utc()),
                ("Server", "Modoki/0.3"),
                ("Connection", "close")
            ]

        if content_type:
            self.headers.pop(0)
            self.headers.append(('Content-type', content_type))

    @staticmethod
    def get_date_string_utc():
        return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
