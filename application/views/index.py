from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView
from application.utils import get_file_content


class IndexView(BaseView):

    def get(self, request: Request) -> Response:
        content_type = self.get_content_type(request)
        content = get_file_content(self.template_dir + "/index.html")
        return Response(body=content, content_type=content_type)
