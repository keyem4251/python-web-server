from application.settings import TEMPLATE_DIR
from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView
from application.utils import get_file_content


class IndexView(BaseView):

    def get(self, request: Request) -> Response:
        content = get_file_content(TEMPLATE_DIR + "/index.html")
        return Response(body=content, content_type="text/html")
