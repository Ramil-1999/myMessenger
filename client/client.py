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
# stat = AuthPage.show(client)
stat = 0
if stat == 1:
    DialogsPage(client)
    pass
elif stat == 2:
    reg_stat = RegPage.show(client)
    if reg_stat:
        if AuthPage.show(client) == 1:
            DialogsPage(client)
            pass

DialogsPage(client)





