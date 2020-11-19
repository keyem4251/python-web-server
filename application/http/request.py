class Request:
    env: dict
    method: str
    path: str
    headers: dict
    cookie: dict
    GET: dict
    POST: dict

    def __init__(self, env: dict):
        self.env = env
        self.method = self.env["REQUEST_METHOD"]
        self.path = self.env["PATH_INFO"]
        self.headers = dict()
        self.headers["CONTENT_TYPE"] = self.env["CONTENT_TYPE"]
        self.headers["CONTENT_LENGTH"] = self.env["CONTENT_LENGTH"]

        for k, v in self.env.items():
            if k.startswith("HTTP_"):
                self.headers[k] = v

        if "HTTP_COOKIE" in self.headers:
            cookies_list = self.headers["HTTP_COOKIE"].split("; ")
            self.cookie = {}
            for cookie in cookies_list:
                key, value = cookie.split("=")
                self.cookie[key] = value

        self.GET = dict()
        self.POST = dict()
        if self.method == "GET" and self.env["QUERY_STRING"]:
            for pair in self.env["QUERY_STRING"].split("&"):
                key, value = pair.split("=")
                self.GET[key] = value
        elif self.method == "POST" and self.headers["CONTENT_TYPE"] == "application/x-www-form-urlencoded":
            for pair in self.body.decode().split("&"):
                key, value = pair.split("=")
                self.POST[key] = value

    @property
    def body(self) -> bytes:
        return self.env["wsgi.input"].read()
