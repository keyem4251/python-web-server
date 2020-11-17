import traceback
from typing import Iterable, List, Callable

from application.http.request import Request
from application.http.response import Response, ResponseNotFound, ResponseServerError
from application.views.parameters import ParametersView
from application.views.headers import HeadersView
from application.views.now import NowView
from application.views.index import IndexView
from application.views.static import StaticView
from application.views.errors import page_not_found, server_error


class WSGIApplication:
    env: dict
    start_response: Callable[[str, List[tuple]], None]

    def create_response(self, request: Request) -> Response:
        try:
            abspath = request.path
            if not abspath.endswith("/") and "." not in abspath:
                path = f"{abspath}/"
            else:
                path = abspath

            if path == "/":
                return IndexView().get_response(request)

            elif path == "/now/":
                return NowView().get_response(request)

            elif path == "/headers/":
                return HeadersView().get_response(request)

            elif path == "/parameters/":
                return ParametersView().get_response(request)

            elif path.startswith("/static/"):
                return StaticView().get_response(request)

            else:
                raise FileNotFoundError

        except FileNotFoundError:
            return page_not_found()

        except Exception:
            print("WsgiApplication 500 Error: " + traceback.format_exc())
            return server_error()

    def set_response_to_start_response(self, response: Response) -> None:
        headers = [(k, v) for k, v in response.headers.items()]
        self.start_response(response.status, headers)

    def application(self, env: dict, start_response: Callable[[str, Iterable[tuple]], None]) -> Iterable[bytes]:
        self.env = env
        self.start_response = start_response

        request = Request(env)
        response: Response = self.create_response(request)
        self.set_response_to_start_response(response)

        return [response.body]
