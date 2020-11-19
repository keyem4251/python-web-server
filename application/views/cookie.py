import json

from application.config import TEMPLATE_DIR
from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView
from application.utils import get_file_content, fill_parameters


class SetCookieView(BaseView):

    def get(self, request: Request) -> Response:
        content = get_file_content(TEMPLATE_DIR + "/cookie/index.html")
        cookie = {
            "test": "12345",
            "test2": "abcde",
        }
        content = fill_parameters(content, {
            "$cookie": json.dumps(cookie)
        })
        response = Response(body=content, content_type="text/html")
        for k, v in cookie.items():
            response.set_cookie(k, v)
        return response
