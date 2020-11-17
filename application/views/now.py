import datetime

from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView


class NowView(BaseView):

    def get(self, request: Request) -> Response:
        content_type = self.get_content_type(request)
        now_bytes = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT').encode()
        content = self.get_file_content(self.template_dir + "/now/index.html")
        content = content.replace(b"$now", now_bytes)

        return Response(body=content, content_type=content_type)
