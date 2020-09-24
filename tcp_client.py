import socket


class TCPClient:
    def main(self):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("通信を開始します。")
        clientsocket.connect(("localhost", 8080))

        # サーバに送信用のメッセージをファイルから読み込む
        with open("client_send.txt", "rb") as f:
            msg = f.read()

        # メッセージを送り返す
        clientsocket.send(msg)

        # サーバーから受け取ったメッセージを代入
        msg = clientsocket.recv(4096)

        # 受け取ったメッセージをファイルに書き込む
        with open("client_recv.txt", "wb") as f:
            f.write(msg)

        clientsocket.close()
        print("通信を終了しました。")


if __name__ == "__main__":
    TCPClient().main()

