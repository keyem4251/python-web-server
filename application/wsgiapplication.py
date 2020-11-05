import os
import datetime
import traceback
from typing import Iterable, List, Callable


class WSGIApplication:
    env: dict
    query: dict
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

    def __init__(self):
        self.env = dict()
        self.query = dict()

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

    @staticmethod
    def parse_parameter(parameter: str) -> dict:
        query = dict()
        if not parameter:
            return query

        for pair in parameter.split("&"):
            key, value = pair.split("=")
            query[key] = value
        return query

    @staticmethod
    def get_ext(abspath: str) -> str:
        if abspath.endswith("/"):
            ext = "html"
        elif not abspath.endswith("/") and "." not in abspath:
            ext = "html"
        else:
            ext = abspath.split(".")[1]
        return ext

    def create_response(self):
        abspath = self.env.get("PATH_INFO")
        root = os.getcwd()
        static_dir = f"{root}/application/static"

        if not abspath.endswith("/") and "." not in abspath:
            path = f"{abspath}/"
        else:
            path = abspath
        ext = self.get_ext(abspath)
        response_headers = self.create_response_headers(ext)

        try:
            if self.env["REQUEST_METHOD"] == "GET":
                query_string = self.env["QUERY_STRING"]
                self.query = self.parse_parameter(query_string)
            elif self.env["REQUEST_METHOD"] == "POST":
                body = self.env['wsgi.input'].read()
                if self.env["CONTENT_TYPE"] == "application/x-www-form-urlencoded":
                    self.query = self.parse_parameter(body.decode())
            print(f"path: {path}")
            if path == "/":
                content = self.get_file_content(static_dir + "/index.html")
                return "200 OK", [content], response_headers

            elif path == "/now/":
                now_bytes = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT').encode()
                content = self.get_file_content(static_dir + "/now/index.html")
                content = content.replace(b"$now", now_bytes)
                return "200 OK", [content], response_headers

            elif path == "/headers/":
                headers_list = [f"{k}: {v}<br>".encode() for k, v in self.env.items()]
                headers_bytes = b"".join(headers_list)
                content = self.get_file_content(static_dir + "/headers/index.html")
                content = content.replace(b"$headers", headers_bytes)
                return "200 OK", [content], response_headers

            elif path == "/parameters/":
                query_list = [f"{k}: {v}<br>".encode() for k, v in self.query.items()]
                query_bytes = b"".join(query_list)
                content = self.get_file_content(static_dir + "/parameters/index.html")
                if self.query:
                    content = content.replace(b"$parameters", query_bytes)
                else:
                    content = content.replace(b"$parameters", b"parameters are not exist")
                return "200 OK", [content], response_headers

            content = self.get_file_content(static_dir + path)
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
