import os
import datetime
import traceback
from typing import Iterable, List, Callable


class WSGIApplication:
    env: dict
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

    def fill_parameter(self, content: bytes):
        if b"$now" in content:
            now_bytes = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT').encode()
            content = content.replace(b"$now", now_bytes)
        if b"$headers" in content:
            headers_list = [f"{k}: {v}<br>\n".encode() for k, v in self.env.items()]
            headers_bytes = b"".join(headers_list)
            content = content.replace(b"$headers", headers_bytes)
        return content

    def create_response(self):
        abspath = self.env.get("PATH_INFO")
        root = os.getcwd()
        static_dir = f"{root}/static"
        ext = abspath.split(".")[1]
        response_headers = self.create_response_headers(ext)

        try:
            if self.env["REQUEST_METHOD"] == "GET":
                query_string = self.env["QUERY_STRING"]
                if query_string:
                    query = dict()
                    for pair in query_string.split("&"):
                        key, value = pair.split("=")
                        query[key] = value
                    
            content = self.get_file_content(static_dir+abspath)
            content = self.fill_parameter(content)
            return "200 OK", [content], response_headers
        except FileNotFoundError:
            not_fount_html = "/404.html"
            content = self.get_file_content(static_dir+not_fount_html)
            return "404 File not Found", [content], response_headers
        except Exception:
            server_error_html = "/500.html"
            content = self.get_file_content(static_dir + server_error_html)
            print("WsgiApplication 500 Error: " + traceback.format_exc())
            return "500 Internal Server Error", [content], response_headers

    def application(self, env: dict, start_response: Callable[[str, Iterable[tuple]], None]) -> Iterable[bytes]:
        self.env = env
        response_code, response_body, response_headers = self.create_response()
        start_response(response_code, response_headers)
        return response_body
