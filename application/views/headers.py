from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import View


class HeadersView(View):

    def get_response(self, request: Request) -> Response:
        if request.method == "GET":
            return self.get(request)

    def get(self, request: Request) -> Response:
        content_type = self.get_content_type(request)
        headers_list = [f"{k}: {v}<br>".encode() for k, v in request.headers.items()]
        headers_bytes = b"".join(headers_list)
        content = self.get_file_content(self.static_dir + "/headers/index.html")
        content = content.replace(b"$headers", headers_bytes)

        return Response(body=content, content_type=content_type)
