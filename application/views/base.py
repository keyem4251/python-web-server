import os

from application.http.request import Request
from application.http.response import Response, HTTP_STATUS


class BaseView:
    content_type: dict
    root: str
    template_dir: str

    def __init__(self):
        self.content_type = {
            "html": "text/html",
            "htm": "text/html",
            "txt": "text/plain",
            "css": "text/css",
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
        }
        self.root = os.getcwd()
        self.template_dir = f"{self.root}/application/templates"

    def get_response(self, request: Request) -> Response:
        if request.method == "GET":
            return self.get(request)

        elif request.method == "POST":
            return self.post(request)
        else:
            return Response(status=HTTP_STATUS.METHOD_NOT_ALLOWED)

    def get(self, request: Request) -> Response:
        return Response(status=HTTP_STATUS.METHOD_NOT_ALLOWED)

    def post(self, request: Request) -> Response:
        return Response(status=HTTP_STATUS.METHOD_NOT_ALLOWED)

    def get_content_type(self, request: Request):
        ext = self.get_ext(request.path)
        return self.content_type.get(ext, "application/octet-stream")

    @staticmethod
    def get_ext(abspath: str) -> str:
        if abspath.endswith("/"):
            ext = "html"
        elif not abspath.endswith("/") and "." not in abspath:
            ext = "html"
        else:
            ext = abspath.split(".")[1]
        return ext
