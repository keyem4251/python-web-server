import os
from application.http.request import Request


class View:
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
