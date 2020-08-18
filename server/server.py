from database_class import Db


class Server:
    def __init__(self, host, port):
        self.db = Db()
        self.port = port
        self.host = host


