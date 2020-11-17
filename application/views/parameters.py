from application.settings import TEMPLATE_DIR
from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView
from application.utils import get_file_content


class ParametersView(BaseView):

    def get(self, request: Request) -> Response:
        query_list = [f"{k}: {v}<br>".encode() for k, v in request.GET.items()]
        query_bytes = b"".join(query_list)
        content = get_file_content(TEMPLATE_DIR + "/parameters/index.html")
        if query_bytes:
            content = content.replace(b"$parameters", query_bytes)
        else:
            content = content.replace(b"$parameters", b"parameters are not exist")
        return Response(body=content, content_type="text/html")

    def post(self, request: Request) -> Response:
        query_list = [f"{k}: {v}<br>".encode() for k, v in request.POST.items()]
        query_bytes = b"".join(query_list)
        content = get_file_content(TEMPLATE_DIR + "/parameters/index.html")
        if query_bytes:
            content = content.replace(b"$parameters", query_bytes)
        else:
            content = content.replace(b"$parameters", b"parameters are not exist")
        return Response(body=content, content_type="text/html")
