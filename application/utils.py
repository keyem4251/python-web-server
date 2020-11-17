import datetime


def get_date_string_utc():
    return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')


def get_file_content(path: str):
    with open(path, "rb") as f:
        return f.read()
