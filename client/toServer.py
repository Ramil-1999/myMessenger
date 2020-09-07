import socket
import json


class ClientBroadcastClass:
    def __init__(self, host, port):
        self.socket = socket.create_connection((host, port))

    def send_data(self, data):
        request = json.dumps(data)
        try:
            self.socket.sendall(request.encode())
            return 1
        except:
            return 0

    def read_data(self):
        message = self.socket.recv(2048)
        return json.loads(message.decode())
