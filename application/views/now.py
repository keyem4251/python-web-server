import datetime

from application.settings import TEMPLATE_DIR
from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView
from application.utils import get_file_content


class NowView(BaseView):

    def get(self, request: Request) -> Response:
        now_bytes = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT').encode()
        content = get_file_content(TEMPLATE_DIR + "/now/index.html")
        content = content.replace(b"$now", now_bytes)

        return Response(body=content, content_type="text/html")
