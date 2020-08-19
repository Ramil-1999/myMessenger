from databaseClass import Db
from logger import Logger
import socket


class Server:
    def __init__(self, host, port):
        self.db = Db()
        self.logger = Logger('log.txt')
        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.socket.listen(1)


