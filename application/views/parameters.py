import os
import datetime
from typing import List

from application.http.request import Request
from application.http.response import Response


class ParametersView:
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

    @staticmethod
    def get_ext(abspath: str) -> str:
        if abspath.endswith("/"):
            ext = "html"
        elif not abspath.endswith("/") and "." not in abspath:
            ext = "html"
        else:
            ext = abspath.split(".")[1]
        return ext

    def get_response(self, request: Request) -> Response:
        abspath = request.path
        root = os.getcwd()
        static_dir = f"{root}/application/static"

        ext = self.get_ext(abspath)
        response_headers = self.create_response_headers(ext)

        if request.method == "GET":
            query_list = [f"{k}: {v}<br>".encode() for k, v in request.GET.items()]
            query_bytes = b"".join(query_list)
            content = self.get_file_content(static_dir + "/parameters/index.html")
            if query_bytes:
                content = content.replace(b"$parameters", query_bytes)
            else:
                content = content.replace(b"$parameters", b"parameters are not exist")
            return Response("200 OK", content, response_headers)

        elif request.method == "POST":
            query_list = [f"{k}: {v}<br>".encode() for k, v in request.POST.items()]
            query_bytes = b"".join(query_list)
            content = self.get_file_content(static_dir + "/parameters/index.html")
            if query_bytes:
                content = content.replace(b"$parameters", query_bytes)
            else:
                content = content.replace(b"$parameters", b"parameters are not exist")
            return Response("200 OK", content, response_headers)
