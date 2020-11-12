import datetime

from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import View


class NowView(View):

    def get_response(self, request: Request) -> Response:
        if request.method == "GET":
            return self.get(request)

    def get(self, request: Request) -> Response:
        content_type = self.get_content_type(request)
        now_bytes = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT').encode()
        content = self.get_file_content(self.static_dir + "/now/index.html")
        content = content.replace(b"$now", now_bytes)

        return Response(body=content, content_type=content_type)
