from application.config import TEMPLATE_DIR
from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView
from application.utils import get_file_content, fill_parameter


class HeadersView(BaseView):

    def get(self, request: Request) -> Response:
        headers_list = [f"{k}: {v}<br>".encode() for k, v in request.headers.items()]
        headers_str = "".join(headers_list)
        content = get_file_content(TEMPLATE_DIR + "/headers/index.html")
        content = fill_parameter(content, "$headers", headers_str)

        return Response(body=content, content_type="text/html")
