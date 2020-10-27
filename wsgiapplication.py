import os
import datetime
from typing import Iterable, List, Callable


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

    def create_response(self, env: dict):
        abspath = env.get("PATH_INFO")
        root = os.getcwd()
        static_dir = f"{root}/static"
        ext = abspath.split(".")[1]
        response_headers = self.create_response_headers(ext)

        try:
            content = self.get_file_content(static_dir+abspath)
            if b"$now" in content:
                now_bytes = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT').encode()
                content = content.replace(b"$now", now_bytes)
            if b"$headers" in content:
                headers_list = [f"{k}: {v}<br>\n".encode() for k, v in env.items()]
                headers_bytes = b"".join(headers_list)
                content = content.replace(b"$headers", headers_bytes)

            return "200 OK", [content], response_headers
        except FileNotFoundError:
            not_fount_html = "/404.html"
            content = self.get_file_content(static_dir+not_fount_html)
            return "404 File not Found", [content], response_headers
        except Exception:
            server_error_html = "/500.html"
            content = self.get_file_content(static_dir + server_error_html)
            return "500 Internal Server Error", [content], response_headers

    def application(self, env: dict, start_response: Callable[[str, Iterable[tuple]], None]) -> Iterable[bytes]:
        response_code, response_body, response_headers = self.create_response(env)
        start_response(response_code, response_headers)
        return response_body
