from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView
from application.utils import get_file_content


class StaticView(BaseView):

    def __init__(self):
        super().__init__()
        self.template_dir = f"{self.root}/application/"

    def get(self, request: Request) -> Response:
        abspath = request.path
        if not abspath.endswith("/") and "." not in abspath:
            path = f"{abspath}/"
        else:
            path = abspath

        content_type = self.get_content_type(request)
        content = get_file_content(self.template_dir + path)
        return Response(content, content_type=content_type)

