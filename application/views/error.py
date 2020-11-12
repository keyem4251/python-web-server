from application.http.request import Request
from application.http.response import Response, ResponseNotFound, ResponseServerError, HTTP_STATUS
from application.views.base import View


class NotFoundView(View):
    not_fount_html: str = "/404.html"

    def __init__(self, template_path=None):
        super().__init__()
        if template_path:
            self.not_fount_html = template_path

    def get_response(self, request: Request) -> Response:
        content = self.get_file_content(self.template_dir + self.not_fount_html)
        return ResponseNotFound(content, content_type="text/html")


class ServerErrorView(View):
    not_fount_html: str = "/500.html"

    def __init__(self, template_path=None):
        super().__init__()
        if template_path:
            self.not_fount_html = template_path

    def get_response(self, request: Request) -> Response:
        content = self.get_file_content(self.template_dir + self.not_fount_html)
        return ResponseServerError(content, content_type="text/html")
