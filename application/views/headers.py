from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView
from application.utils import get_file_content


class HeadersView(BaseView):

    def get(self, request: Request) -> Response:
        content_type = self.get_content_type(request)
        headers_list = [f"{k}: {v}<br>".encode() for k, v in request.headers.items()]
        headers_bytes = b"".join(headers_list)
        content = get_file_content(self.template_dir + "/headers/index.html")
        content = content.replace(b"$headers", headers_bytes)

        return Response(body=content, content_type=content_type)
