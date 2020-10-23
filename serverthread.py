import socket
import traceback
import os
from threading import Thread
from typing import List, Iterable

from wsgiapplication import WSGIApplication


class ServerThread(Thread):
    separator = "\r\n"
    response_line: str
    response_headers: List[tuple]

    def __init__(self, client_socket: socket):
        super().__init__()
        self.socket = client_socket

    @staticmethod
    def get_response_body(body_bytes_list) -> bytes:
        return b"\r\n" + b"".join(body_bytes_list)

    def get_response_headers(self) -> bytes:
        headers = [f"HTTP/1.1 {self.response_line}"]
        for response_header in self.response_headers:
            headers.append(f"{response_header[0]}: {response_header[1]}")
        return "\r\n".join(headers).encode()

    def run(self) -> None:
        try:
            # クライアントから受け取ったメッセージを代入
            request = self.socket.recv(4096)
            print("-------------- receive request --------------")
            print(request.decode())
            print("---------------------------------------------")

            lines = request.decode().split(self.separator)

            method = lines[0].split(" ")[0]
            abspath = os.path.abspath(lines[0].split(" ")[1])
            protocol = lines[0].split(" ")[2]
            query_string = abspath.split("?")[1] if "?" in abspath else ""

            # envを作る
            # content-type, content-lengthはhttpリクエストに入っている場合は取得する
            env = {
                "REQUEST_METHOD": method,
                "SERVER_PROTOCOL": protocol,
                "PATH_INFO": abspath,
                "QUERY_STRING": query_string,
                "CONTENT_TYPE": "",
                "CONTENT_LENGTH": "",
                "wsgi.input": "",
                "wsgi.url_scheme": "http",
            }

            def start_response(response_line: str, response_headers: List[tuple]):
                self.response_line = response_line
                self.response_headers = response_headers

            # WSGIApplication.applicationにわたす
            body_bytes_list: Iterable[bytes] = WSGIApplication().application(env, start_response)

            # WSGIApplicationのapplicationの戻り値を元にレスポンスを作る
            output_bytes = b""
            output_bytes += self.get_response_headers()
            output_bytes += "\r\n".encode()
            output_bytes += self.get_response_body(body_bytes_list)
            print(f"output_bytes: {output_bytes}")
            self.socket.send(output_bytes)

        except Exception:
            print(traceback.format_exc())

        finally:
            self.socket.close()
            print("通信を終了しました。")
