from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import View


class ParametersView(View):

    def get_response(self, request: Request) -> Response:
        if request.method == "GET":
            return self.get(request)

        elif request.method == "POST":
            return self.post(request)

    def get(self, request: Request) -> Response:
        content_type = self.get_content_type(request)
        query_list = [f"{k}: {v}<br>".encode() for k, v in request.GET.items()]
        query_bytes = b"".join(query_list)
        content = self.get_file_content(self.static_dir + "/parameters/index.html")
        if query_bytes:
            content = content.replace(b"$parameters", query_bytes)
        else:
            content = content.replace(b"$parameters", b"parameters are not exist")
        return Response(body=content, content_type=content_type)

    def post(self, request: Request) -> Response:
        content_type = self.get_content_type(request)
        query_list = [f"{k}: {v}<br>".encode() for k, v in request.POST.items()]
        query_bytes = b"".join(query_list)
        content = self.get_file_content(self.static_dir + "/parameters/index.html")
        if query_bytes:
            content = content.replace(b"$parameters", query_bytes)
        else:
            content = content.replace(b"$parameters", b"parameters are not exist")
        return Response(body=content, content_type=content_type)
