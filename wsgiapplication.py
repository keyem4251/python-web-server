import os
import datetime
from typing import Iterable, List


class WSGIApplication:
    content_type = {
        "html": "text/html",
        "htm": "text/html",
        "txt": "text/plain",
        "css": "text/css",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
    }

    def get_content_type(self, ext: str):
        return self.content_type.get(ext, "application/octet-stream")

    @staticmethod
    def get_date_string_utc():
        return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

    @staticmethod
    def get_file_content(path: str):
        with open(path, "rb") as f:
            return f.read()

    def create_response_headers(self, ext: str) -> List:
        response_headers = [
            ('Content-type', self.get_content_type(ext)),
            ("Date", self.get_date_string_utc()),
            ("Server", "Modoki/0.3"),
            ("Connection", "close")
        ]
        return response_headers

    def create_response(self, abspath: str):
        root = os.getcwd()
        static_dir = f"{root}/static"
        ext = abspath.split(".")[1]
        response_headers = self.create_response_headers(ext)

        try:
            content = self.get_file_content(static_dir+abspath)
            return "200 OK", [content], response_headers
        except FileNotFoundError:
            not_fount_html = "/404.html"
            content = self.get_file_content(static_dir+not_fount_html)
            return "404 File not Found", [content], response_headers
        except Exception:
            return "500 Internal Server Error", [b""], response_headers

    def application(self, env: dict, start_response) -> Iterable[bytes]:
        abspath = env.get("PATH_INFO")
        response_code, response_body, response_headers = self.create_response(abspath)
        start_response(response_code, response_headers)
        return response_body
