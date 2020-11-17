from application.settings import STATIC_DIR
from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView
from application.utils import get_file_content


class StaticView(BaseView):
    content_type: dict

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

    def get(self, request: Request) -> Response:
        filename = request.path.replace("/static/", "")
        content_type = self.get_content_type(request)
        content = get_file_content(STATIC_DIR + filename)
        return Response(content, content_type=content_type)

