from application.http.request import Request
from application.http.response import Response


class ParametersView:
    def get_response(self, request: Request) -> Response:
        abspath = request.path
        root = os.getcwd()
        static_dir = f"{root}/application/static"

        ext = self.get_ext(abspath)
        response_headers = self.create_response_headers(ext)

        if request.method == "GET":
            query_list = [f"{k}: {v}<br>".encode() for k, v in request.GET.items()]
            query_bytes = b"".join(query_list)
            content = self.get_file_content(static_dir + "/parameters/index.html")
            if query_bytes:
                content = content.replace(b"$parameters", query_bytes)
            else:
                content = content.replace(b"$parameters", b"parameters are not exist")
            return Response("200 OK", content, response_headers)

        elif request.method == "POST":
            query_list = [f"{k}: {v}<br>".encode() for k, v in request.POST.items()]
            query_bytes = b"".join(query_list)
            content = self.get_file_content(static_dir + "/parameters/index.html")
            if query_bytes:
                content = content.replace(b"$parameters", query_bytes)
            else:
                content = content.replace(b"$parameters", b"parameters are not exist")
            return Response("200 OK", content, response_headers)
