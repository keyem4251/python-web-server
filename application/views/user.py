from hashlib import sha256

from application.config import TEMPLATE_DIR
from application.http.request import Request
from application.http.response import Response, HTTP_STATUS
from application.views.base import BaseView
from application.utils import get_file_content, fill_parameters
from application.sessions import SESSIONS


class UserView(BaseView):

    def get(self, request: Request) -> Response:
        content = get_file_content(TEMPLATE_DIR + "/user/index.html")
        user_id = request.cookies.get("session_id")

        user_name = "名無し"
        if user_id is not None:
            user_name = SESSIONS.get(user_id)
        content = fill_parameters(content, {"$user_name": user_name})
        return Response(body=content, content_type="text/html")

    def post(self, request: Request) -> Response:
        user_name = request.POST["user_name"]

        if "session_id" in request.cookies:
            user_id = request.cookies.get("session_id")
        else:
            user_id = sha256(user_name.encode()).hexdigest()
            SESSIONS[user_id] = user_name

        content = get_file_content(TEMPLATE_DIR + "/user/index.html")
        content = fill_parameters(content, {"$user_name": user_name})
        response = Response(body=content, content_type="text/html")
        response.set_cookie("session_id", user_id)
        return response
