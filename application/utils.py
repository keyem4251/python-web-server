import datetime


def get_date_string_utc():
    return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')


def get_file_content(path: str):
    with open(path, "rb") as f:
        return f.read()


def add_slash(path: str):
    if not path.endswith("/") and "." not in path:
        return f"{path}/"
    return path


def fill_parameters(content: bytes, items: dict) -> bytes:
    for k, v in items.items():
        content = content.replace(k.encode(), v.encode())
    return content
