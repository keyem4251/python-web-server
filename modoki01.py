import socket
import datetime
import os


class Modoki01:

    separator = "\r\n"

    @staticmethod
    def get_date_string_utc():
        return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

    def write_line(self, response, msg=None):
        if msg is None:
            response += self.separator
        else:
            response += f"{msg}{self.separator}"
        return response

    def main(self):
        # create an INET, STREAMing socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to a public host, and a well-known port
        serversocket.bind(("localhost", 8080))
        # become a server socket
        serversocket.listen(1)

        print("クライントからの接続を待ちます。")
        (clientsocket, address) = serversocket.accept()
        print("クライント接続。")

        # クライアントから受け取ったメッセージを代入
        request = clientsocket.recv(4096)
        lines = request.decode().split(self.separator)
        path = ""

        if "GET" in lines[0]:
            path = lines[0].split(" ")[1]

        # レスポンスヘッダを返す
        utc_date = self.get_date_string_utc()
        response = ""
        response = self.write_line(response, "HTTP/1.1 200 OK")
        response = self.write_line(response, f"Date:{utc_date}")
        response = self.write_line(response, "Server: Modoki/0.1")
        response = self.write_line(response, "Connection: close")
        response = self.write_line(response, "Content-type: text/html")
        response = self.write_line(response)

        # レスポンスボディを返す
        root = os.getcwd()
        static_dir = f"{root}/static"
        with open(static_dir+path, "rb") as f:
            content = f.read()
            response += content.decode()

        # メッセージを送り返す
        clientsocket.send(response.encode())

        clientsocket.close()
        print("通信を終了しました。")


if __name__ == "__main__":
    Modoki01().main()
