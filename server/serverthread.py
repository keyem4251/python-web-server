import socket
import traceback
import os
import io
from threading import Thread
from typing import List, Iterable

from application.wsgiapplication import WSGIApplication
from server.message import Request


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

    @staticmethod
    def build_env(message: bytes):
        request = Request()
        request.parse(message)

        env = {
            "REQUEST_METHOD": request.method,
            "SERVER_PROTOCOL": request.protocol,
            "PATH_INFO": request.path,
            "QUERY_STRING": request.query_string,
            "CONTENT_TYPE": request.content_type,
            "CONTENT_LENGTH": request.content_length,
            "SERVER_NAME": request.server_name,
            "SERVER_PORT": request.server_port,
            "wsgi.input": io.BytesIO(request.body),
        }
        for k, v in request.http_variables.items():
            key = "HTTP_" + k.upper().replace("-", "_")
            env[key] = v
        return env

    def build_response(self, body_bytes_list: Iterable[bytes]):
        # WSGIApplicationのapplicationの戻り値を元にレスポンスを作る
        output_bytes = b""
        output_bytes += self.get_response_headers()
        output_bytes += "\r\n".encode()
        output_bytes += self.get_response_body(body_bytes_list)
        return output_bytes

    def run(self) -> None:
        try:
            message = self.socket.recv(4096)
            print("-------------- receive request --------------")
            print(message.decode())
            print("---------------------------------------------")

            # requestを元にenvを作成
            env = self.build_env(message)

            # start_responseを定義
            def start_response(response_line: str, response_headers: List[tuple]):
                self.response_line = response_line
                self.response_headers = response_headers

            # WSGIApplication.applicationにわたす
            body_bytes_list: Iterable[bytes] = WSGIApplication().application(env, start_response)

            response = self.build_response(body_bytes_list)
            print("-------------- send response --------------")
            print(response.decode())
            print("---------------------------------------------")
            self.socket.send(response)

        except Exception:
            print(traceback.format_exc())

        finally:
            self.socket.close()
            print("通信を終了しました。")
