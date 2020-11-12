import os
import datetime
import traceback
from typing import Iterable, List, Callable

from application.http.request import Request
from application.http.response import Response, ResponseNotFound, ResponseServerError
from application.views.parameters import ParametersView
from application.views.headers import HeadersView
from application.views.now import NowView
from application.views.error import NotFoundView, ServerErrorView


class WSGIApplication:
    env: dict
    start_response: Callable[[str, List[tuple]], None]

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

    def create_response_headers(self, ext: str) -> dict:
        response_headers = {
            "Content-type": self.get_content_type(ext),
            "Date": self.get_date_string_utc(),
            "Server": "HenaDjango",
            "Connection": "close",
        }
        return response_headers

    @staticmethod
    def get_ext(abspath: str) -> str:
        if abspath.endswith("/"):
            ext = "html"
        elif not abspath.endswith("/") and "." not in abspath:
            ext = "html"
        else:
            ext = abspath.split(".")[1]
        return ext

    def create_response(self, request: Request) -> Response:
        abspath = request.path
        root = os.getcwd()
        static_dir = f"{root}/application/static"

        if not abspath.endswith("/") and "." not in abspath:
            path = f"{abspath}/"
        else:
            path = abspath
        ext = self.get_ext(abspath)
        response_headers = self.create_response_headers(ext)

        try:
            if path == "/":
                content = self.get_file_content(static_dir + "/index.html")
                return Response(content, headers=response_headers)

            elif path == "/now/":
                return NowView().get_response(request)

            elif path == "/headers/":
                return HeadersView().get_response(request)

            elif path == "/parameters/":
                return ParametersView().get_response(request)

            content = self.get_file_content(static_dir + path)
            return Response(content, headers=response_headers)

        except FileNotFoundError:
            return NotFoundView().get_response(request)
        except Exception:
            print("WsgiApplication 500 Error: " + traceback.format_exc())
            return ServerErrorView().get_response(request)

    def start_response_from_response(self, response: Response) -> None:
        headers = [(k, v) for k, v in response.headers.items()]
        self.start_response(response.status, headers)

    def application(self, env: dict, start_response: Callable[[str, Iterable[tuple]], None]) -> Iterable[bytes]:
        self.env = env
        self.start_response = start_response

        request = Request(env)
        response: Response = self.create_response(request)
        self.start_response_from_response(response)

        return [response.body]
