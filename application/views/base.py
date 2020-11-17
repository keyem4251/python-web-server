from application.http.request import Request
from application.http.response import Response, HTTP_STATUS


class BaseView:
    def get_response(self, request: Request) -> Response:
        if request.method == "GET":
            return self.get(request)

        elif request.method == "POST":
            return self.post(request)

        else:
            return Response(status=HTTP_STATUS.METHOD_NOT_ALLOWED)

    def get(self, request: Request) -> Response:
        return Response(status=HTTP_STATUS.METHOD_NOT_ALLOWED)

    def post(self, request: Request) -> Response:
        return Response(status=HTTP_STATUS.METHOD_NOT_ALLOWED)
