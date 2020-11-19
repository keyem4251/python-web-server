import os

from application.config import TEMPLATE_DIR
from application.http.response import Response, ResponseNotFound, ResponseServerError
from application.utils import get_file_content


def page_not_found(template_name="/404.html") -> Response:
    content = get_file_content(TEMPLATE_DIR+template_name)
    return ResponseNotFound(content, content_type="text/html")


def server_error(template_name="/500.html") -> Response:
    content = get_file_content(TEMPLATE_DIR+template_name)
    return ResponseServerError(content, content_type="text/html")
