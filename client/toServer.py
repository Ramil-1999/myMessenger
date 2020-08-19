import socket
import json


class ClientBroadcastClass:
    def __init__(self, host, port):
        self.socket = socket.create_connection((host, port))
        print("connected")

    def send_info(self, data):
        request = json.dumps(data)
        try:
            self.socket.sendall(request.encode())
            return 1
        except:
            return 0
