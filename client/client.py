from authPage import *
from toServer import *
from dialogPage import *
# cd Documents\projects\pycharm\myMessenger\server


class Client:
    def __init__(self):
        self.broadcast = ClientBroadcastClass('127.0.0.1', 10001)


client = Client()
AuthPage(client.broadcast)
DialogPage(client.broadcast)



