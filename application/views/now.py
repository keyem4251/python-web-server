import datetime

from application.config import TEMPLATE_DIR
from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView
from application.utils import get_file_content, fill_parameters


class NowView(BaseView):

    def get(self, request: Request) -> Response:
        utc_now_str = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        content = get_file_content(TEMPLATE_DIR + "/now/index.html")
        content = fill_parameters(content, {"$now": utc_now_str})

        return Response(body=content, content_type="text/html")
