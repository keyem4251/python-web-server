from application.settings import STATIC_DIR
from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView
from application.utils import get_file_content


class StaticView(BaseView):

    def get(self, request: Request) -> Response:
        filename = request.path.replace("/static/", "")
        content_type = self.get_content_type(request)
        content = get_file_content(STATIC_DIR + filename)
        return Response(content, content_type=content_type)

