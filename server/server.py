from databaseClass import *
from logger import Logger
import socket
import json


class Server:
    def __init__(self, host, port):
        self.db = Db()
        self.logger = Logger('log.txt')
        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.socket.listen(1)

    def send_data(self, message):
        request = json.dumps(message)
        self.socket.sendall(request.encode())

    def auth(self, message):
        try:
            result = self.db.find_user(message['username'])
            if result != -1:
                if result == message['hash']:
                    return 1
        except Error:
            self.logger.logging('Database connection refused')
            return -1

    def reg(self, message):
        pass