from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import View


class StaticView(View):
    static_dir: str

    def __init__(self):
        super().__init__()
        self.static_dir = f"{self.root}/application/"

    def get_response(self, request: Request) -> Response:
        abspath = request.path
        if not abspath.endswith("/") and "." not in abspath:
            path = f"{abspath}/"
        else:
            path = abspath

        content_type = self.get_content_type(request)
        content = self.get_file_content(self.static_dir + path)
        return Response(content, content_type=content_type)
