import socket
import traceback
import os
import io
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

    def parse_request(self, request_str: str):
        request_line, remain = request_str.split(self.separator, maxsplit=1)
        headers, body = remain.rsplit(self.separator, maxsplit=1)
        return request_line, headers, body

    @staticmethod
    def parse_request_line(request_line: str):
        method, path, protocol = request_line.split(" ", maxsplit=2)
        abspath = os.path.abspath(path)
        query_string = ""
        if "?" in abspath:
            abspath, query_string = abspath.split("?", maxsplit=1)
        return method, abspath, protocol, query_string

    def parse_headers(self, headers: str):
        headers_dict = dict()
        for header in headers.split(self.separator):
            if ": " in header:
                key, value = header.split(": ")
                headers_dict[key] = value
        server_name, server_port = headers_dict.pop("Host", "").split(":")
        content_type = headers_dict.pop("Content-Type", "")
        content_length = headers_dict.pop("Content-Length", "")
        return server_name, server_port, content_type, content_length, headers_dict

    def build_env(self, request_str: str):
        request_line, headers, body = self.parse_request(request_str)
        method, abspath, protocol, query_string = self.parse_request_line(request_line)
        server_name, server_port, content_type, content_length, http_variables_dict = self.parse_headers(headers)

        env = {
            "REQUEST_METHOD": method,
            "SERVER_PROTOCOL": protocol,
            "PATH_INFO": abspath,
            "QUERY_STRING": query_string,
            "CONTENT_TYPE": content_type,
            "CONTENT_LENGTH": content_length,
            "SERVER_NAME": server_name,
            "SERVER_PORT": server_port,
            "wsgi.input": io.StringIO(body),
        }
        for k, v in http_variables_dict.items():
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
            request = self.socket.recv(4096)
            print("-------------- receive request --------------")
            print(request.decode())
            print("---------------------------------------------")

            # requestを元にenvを作成
            env = self.build_env(request.decode())

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
