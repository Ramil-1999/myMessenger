from databaseClass import *
from logger import Logger
import asyncio
import json


class Server(asyncio.Protocol):
    def __init__(self):
        super().__init__()
        self.db = Db()
        self.logger = Logger('log.txt')

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        """Метод data_received вызывается при получении данных в сокете"""
        try:
            request = json.loads(data.decode())

            # отработка запроса на авторизацию
            if request['type'] == 'auth':
                result = self.auth(request)
                if result == 1:
                    response = {'status': 'ok'}
                elif result == -1:
                    response = {'status': 'password'}
                else:
                    response = {'status': 'username'}

            # отработка запроса на регистрацию
            elif request['type'] == 'reg':
                result = self.reg(request['username'], request['hash'])
                if result == 1:
                    response = {'status': 'ok'}
                else:
                    response = {'status': 'username'}

            # отработка запроса на полученме чатов у пользователя
            elif request['type'] == 'get_chats':
                result = self.get_chats(request['user_id'])
                response = result

        except (ValueError, UnicodeDecodeError, IndexError):
            print('error')

        self.transport.write(json.dumps(response).encode())

    def auth(self, message):
        try:
            result = self.db.find_user(message['username'])
            if result == message['hash']:
                return 1
            elif result == 0:
                return 0
            else:
                return -1
        except Error:
            self.logger.logging('Database connection refused')
            return -1

    def reg(self, username, hash):
        result = self.db.reg_user(username, hash)
        if result:
            return 1
        else:
            return 0

    def get_chats(self, user_id):
        result = self.db.get_chats(user_id)
        return result
