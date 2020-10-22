import os
import datetime
from typing import Iterable


class WSGIApplication:
    content_type = {
        "html": "text/html",
        "htm": "text/html",
        "txt": "text/plain",
        "css": "text/css",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
    }

    def get_content_type(self, ext: str):
        return self.content_type.get(ext, "application/octet-stream")

    @staticmethod
    def get_date_string_utc():
        return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

    @staticmethod
    def get_file_content(path: str):
        with open(path, "rb") as f:
            return f.read()

    def application(self, env: dict, start_response) -> Iterable[bytes]:
        """
                env:
                    リクエストヘッダーの情報がdictで渡されてくる
                    refs) https://www.python.org/dev/peps/pep-3333/#environ-variables
                    例）
                    env = {
                        "HTTP_METHOD": "POST",
                        "PATH_INFO": "/index.html"
                    }
        ​
                start_response:
                    レスポンスヘッダーの内容を、WSGIサーバーへ伝えるための関数(or Callable)。
                    WSGIアプリケーション内で一度だけコールする。
                    コールするときは、第一引数にレスポンスライン、第２引数にレスポンスヘッダーを渡してコールする。
                    例）
                    start_response(
                        '200 OK',
                        [
                            ('Content-type', 'text/plain; charset=utf-8'),
                            ('Connection', 'Closed')
                        ]
                    )
        """
        response_headers = []
        # Content-typeはenvから作る
        abspath = env.get("PATH_INFO")
        ext = abspath.split(".")[1]
        response_headers.append(('Content-type', self.get_content_type(ext)))
        response_headers.append(("Date", self.get_date_string_utc()))
        response_headers.append(("Server", "Modoki/0.3"))
        response_headers.append(("Connection", "close"))

        response_code = "200 OK"
        content = b""

        # envを見てファイルを開いてレスポンスボディを返す
        root = os.getcwd()
        static_dir = f"{root}/static"

        try:
            content = self.get_file_content(static_dir+abspath)
        except FileNotFoundError:
            response_code = "404 File not Found"
            not_fount_html = f"{root}/static/404.html"
            content = self.get_file_content(not_fount_html)
        except Exception:
            response_code = "500 Internal Server Error"

        start_response(response_code, response_headers)
        return [content]
