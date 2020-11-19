from application.config import TEMPLATE_DIR
from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView
from application.utils import get_file_content, fill_parameter


class SetCookieView(BaseView):

    def get(self, request: Request) -> Response:
        content = get_file_content(TEMPLATE_DIR + "/cookie/index.html")
        key = "test"
        value = "value"
        content = fill_parameter(content, "$key", key)
        content = fill_parameter(content, "$value", value)
        response = Response(body=content, content_type="text/html")
        response.set_cookie(key, value)
        response.set_cookie("test2", "value2")
        return response
