from authPage import *
from toServer import *
from dialogsPage import *
from logger import *
# cd Documents\projects\pycharm\myMessenger\server


class Client:
    def __init__(self):
        self.broadcast = ClientBroadcastClass('127.0.0.1', 10001)
        self.logger = Logger("log.txt")


client = Client()
AuthPage(client)
DialogsPage(client)




