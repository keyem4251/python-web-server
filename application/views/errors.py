import os

from application.http.response import Response, ResponseNotFound, ResponseServerError
from application.utils import get_file_content


def page_not_found(template_name="/404.html") -> Response:
    root = os.getcwd()
    template_dir = f"{root}/application/templates"
    content = get_file_content(template_dir+template_name)
    return ResponseNotFound(content, content_type="text/html")


def server_error(template_name="/500.html") -> Response:
    root = os.getcwd()
    template_dir = f"{root}/application/templates"
    content = get_file_content(template_dir+template_name)
    return ResponseServerError(content, content_type="text/html")
