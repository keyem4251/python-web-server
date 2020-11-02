import os


class Request:
    separator: str
    body: bytes
    method: str
    path: str
    protocol: str
    query_string: str
    server_name: str
    server_port: str
    content_type: str
    content_length: str
    http_variables: dict

    def __init__(self):
        self.separator = "\r\n"
        self.body = None
        self.method = None
        self.path = None
        self.protocol = None
        self.query_string = None
        self.server_name = None
        self.server_port = None
        self.content_type = None
        self.content_length = None
        self.http_variables = dict()

    def parse_request(self, request_str: str):
        request_line, remain = request_str.split(self.separator, maxsplit=1)
        headers, body_str = remain.rsplit(self.separator, maxsplit=1)
        return request_line, headers, body_str.encode()

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

    def parse(self, message: bytes):
        message_str = message.decode()
        request_line, headers, self.body = self.parse_request(message_str)
        self.method, self.path, self.protocol, self.query_string = self.parse_request_line(request_line)
        self.server_name, self.server_port, self.content_type, self.content_length, self.http_variables = self.parse_headers(headers)
