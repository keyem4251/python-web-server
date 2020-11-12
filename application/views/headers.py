import os

from application.http.request import Request
from application.http.response import Response, HTTP_STATUS


class HeadersView:
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
    root = os.getcwd()
    static_dir = f"{root}/application/static"

    def get_content_type(self, request: Request):
        ext = self.get_ext(request.path)
        return self.content_type.get(ext, "application/octet-stream")

    @staticmethod
    def get_file_content(path: str):
        with open(path, "rb") as f:
            return f.read()

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
        if request.method == "GET":
            return self.get(request)

    def get(self, request: Request) -> Response:
        content_type = self.get_content_type(request)
        headers_list = [f"{k}: {v}<br>".encode() for k, v in request.headers.items()]
        headers_bytes = b"".join(headers_list)
        content = self.get_file_content(self.static_dir + "/headers/index.html")
        content = content.replace(b"$headers", headers_bytes)

        return Response(status=HTTP_STATUS.OK, body=content, content_type=content_type)
