from databaseClass import Db
import socket


class Server:
    def __init__(self, host, port):
        self.db = Db()
        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.socket.listen(1)


