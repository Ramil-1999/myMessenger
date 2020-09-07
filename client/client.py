from authPage import *
from toServer import *
from dialogsPage import *
from logger import *
from datetime import datetime
# cd Documents\projects\pycharm\myMessenger\server


class Client:
    def __init__(self):
        self.broadcast = ClientBroadcastClass('127.0.0.1', 10001)
        self.logger = Logger("log.txt")
        self.user_id = None

    def ask_chats(self):
        request = {
            'type': 'get_chats',
            'user_id': self.user_id
        }
        self.broadcast.send_data(request)
        return self.broadcast.read_data()

    def ask_history(self, chat_id):
        request = {
            'type': 'get_history',
            'chat_id': chat_id
        }
        self.broadcast.send_data(request)
        result = self.broadcast.read_data()
        return result

    def send_message(self, *msg):
        time = datetime.now()
        request = {
            'type': 'send_message',
            'chat_id': msg[0],
            'user_id': msg[1],
            'content': msg[2],
            'time': str(time)
        }
        self.broadcast.send_data(request)
        response = self.broadcast.read_data()

    def add_chat(self, username):
        request = {
            'type': 'add_chat',
            'username': username,
            'user_id': self.user_id
        }
        self.broadcast.send_data(request)
        response = self.broadcast.read_data()
        if response['status'] == 'ok':
            return 1

    def ask_user_data(self, user_id):
        request = {
            'type': 'get_user_data',
            'user_id': user_id
        }
        self.broadcast.send_data(request)
        response = self.broadcast.read_data()
        if response['status'] == 'ok':
            return response['name'], response['surname']


client = Client()
stat = AuthPage.show(client)

if stat == 1:
    DialogsPage(client)
    pass
elif stat == 2:
    reg_stat = RegPage.show(client)
    if reg_stat:
        if AuthPage.show(client) == 1:
            DialogsPage(client)
            pass
