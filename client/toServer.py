import socket


class ClientBroadcastClass:
    def __init__(self, host, port):
        self.socket = socket.create_connection((host, port))
        print("connected")

    def send_info(self, data):
        try:
            self.socket.sendall(data.encode())
            return 1
        except:
            return 0
