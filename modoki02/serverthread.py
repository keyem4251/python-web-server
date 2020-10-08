import socket
import datetime
import os
import traceback
from threading import Thread


class ServerThread(Thread):

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
    separator = "\r\n"

    def __init__(self, client_socket: socket):
        super().__init__()
        self.socket = client_socket

    @staticmethod
    def get_date_string_utc():
        return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

    def write_line(self, response: str, msg=None):
        if msg is None:
            response += self.separator
        else:
            response += f"{msg}{self.separator}"
        return response

    def get_content_type(self, ext: str):
        return self.content_type.get(ext, "application/octet-stream")

    @staticmethod
    def get_file_content(path: str):
        with open(path, "rb") as f:
            return f.read()

    def run(self) -> None:
        try:
            # クライアントから受け取ったメッセージを代入
            request = self.socket.recv(4096)
            lines = request.decode().split(self.separator)

            abspath = os.path.abspath(lines[0].split(" ")[1])
            ext = abspath.split(".")[1]

            # レスポンスヘッダを返す
            utc_date = self.get_date_string_utc()
            response = ""
            response = self.write_line(response, "HTTP/1.1 200 OK")
            response = self.write_line(response, f"Date:{utc_date}")
            response = self.write_line(response, "Server: Modoki/0.2")
            response = self.write_line(response, "Connection: close")
            response = self.write_line(response, "Content-type: " + self.get_content_type(ext))
            response = self.write_line(response)

            # レスポンスボディを返す
            root = os.getcwd()
            static_dir = f"{root}/../static"
            content = self.get_file_content(static_dir+abspath)

            # メッセージを送り返す
            self.socket.send(response.encode() + content)

        except FileNotFoundError:
            # ファイルが存在しない場合のレスポンスヘッダを作成
            utc_date = self.get_date_string_utc()
            response = ""
            response = self.write_line(response, "HTTP/1.1 404 Not Found")
            response = self.write_line(response, f"Date:{utc_date}")
            response = self.write_line(response, "Server: Modoki/0.2")
            response = self.write_line(response, "Connection: close")
            response = self.write_line(response, "Content-type: text/html")
            response = self.write_line(response)

            root = os.getcwd()
            not_fount_html = f"{root}/../static/404.html"
            content = self.get_file_content(not_fount_html)

            # メッセージを送り返す
            self.socket.send(response.encode() + content)

        except Exception:
            print(traceback.format_exc())

        finally:
            self.socket.close()
            print("通信を終了しました。")
