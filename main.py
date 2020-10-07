import socket
from serverthread import ServerThread


class Main:

    @staticmethod
    def main():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to a public host, and a well-known port
        server_socket.bind(("localhost", 8080))
        # become a server socket
        server_socket.listen(1)

        while True:
            print("クライントからの接続を待ちます。")
            (client_socket, address) = server_socket.accept()
            print("クライント接続。")

            thread = ServerThread(client_socket)
            print("スレッド起動。")
            thread.start()


if __name__ == "__main__":
    Main().main()
