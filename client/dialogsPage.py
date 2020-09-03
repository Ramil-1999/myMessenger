from tkinter import *
from tkinter.scrolledtext import *
import scrollableFrame
from datetime import datetime


# класс страницы всех чатов
class DialogsPage:
    def __init__(self, client):
        self.client = client
        self.chats = []
        self.messages = []
        self.root = Tk()
        self.root.resizable(width=FALSE, height=FALSE)
        self.root.title('Dialogs')
        self.root.geometry("{0}x{1}+{2}+{3}".format(400, 600, int((self.root.winfo_screenwidth() - 400)/2),
                                                    int((self.root.winfo_screenheight() - 600)/2)))
        self.create_widgets()

    # создание страницы списка всех чатов данного пользователя
    def create_widgets(self):
        self.ask_chats()
        self.frame1 = Frame()

        frame_top = Frame(self.frame1)
        Button(frame_top, text='+', width=100, command=self.window_add_chat).pack()
        frame_top.pack(side='top')

        frame_main = scrollableFrame.ScrollableFrame(self.frame1, 0)

        # вывод всех доступных чатов
        for chat in self.chats:
            txt = self.make_text_for_button(chat)
            Button(frame_main.scrollable_frame, width='100', text=txt,
                   command=lambda n=chat: self.open_chat(n), height=4, anchor='w').pack(fill=X)
        frame_main.pack(fill=BOTH, expand=1)
        self.frame1.pack(expand=1, fill=BOTH)
        self.root.mainloop()

    # создание страницы открытого чата
    def open_chat(self, chat):
        chat_id = chat['chat_id']
        name = chat['name']
        surname = chat['surname']

        self.frame1.destroy()
        # верстка экрана чата
        frame2 = Frame(self.root)

        # шапка из кнопки возврата и имени пользователя на той стороне чата)
        frame_top = Frame(frame2)
        Button(frame_top, text='<--', width=10, command=lambda: (frame2.destroy(), self.create_widgets()))\
            .pack(side='left')
        Label(frame_top, text='{0} {1}'.format(name, surname), width=90).pack(side='right')
        frame_top.pack(side='top')

        # фрейм в котором отображаются сообщения
        frame_mid = scrollableFrame.ScrollableFrame(frame2, 1)
        self.messages = self.ask_history(chat_id)
        for message in self.messages:
            if self.client.user_id == message['user_id']:
                Label(frame_mid.scrollable_frame, text=message['content'], anchor='e', width=50).pack()
            else:
                Label(frame_mid.scrollable_frame, text=message['content'], anchor='w', width=55).pack()
        frame_mid.pack(fill=BOTH, expand=1)

        # фрейм-хвост
        frame_bottom = Frame(frame2)
        text_field = ScrolledText(frame_bottom, width=40, height=2)
        text_field.pack(side='left')

        Button(frame_bottom, command=lambda: (self.send_message(chat_id, name, surname,  self.client.user_id, text_field.get(1.0, END)), frame2.destroy()), text='send').pack(side='right')
        frame_bottom.pack(side='bottom')
        frame2.pack(fill=Y, expand=1)

    def ask_chats(self):
        request = {
            'type': 'get_chats',
            'user_id': self.client.user_id
        }
        self.client.broadcast.send_data(request)
        self.chats = self.client.broadcast.read_data()

    def ask_history(self, chat_id):
        request = {
            'type': 'get_history',
            'chat_id': chat_id
        }
        self.client.broadcast.send_data(request)
        result = self.client.broadcast.read_data()
        return result

    def send_message(self, chat_id, name, surname, user_id, content):
        time = datetime.now()
        request = {
            'type': 'send_message',
            'chat_id': chat_id,
            'user_id': user_id,
            'content': content,
            'time': str(time)
        }
        self.client.broadcast.send_data(request)
        response = self.client.broadcast.read_data()
        chat = {
            'chat_id': chat_id,
            'name': name,
            'surname': surname
        }
        self.open_chat(chat)

    def window_add_chat(self):
        root2 = Toplevel()
        root2.title('Create New Chat')
        root2.geometry("{0}x{1}+{2}+{3}".format(200, 200, int((self.root.winfo_screenwidth() - 200) / 2),
                                                int((self.root.winfo_screenheight() - 200) / 2)))
        Label(root2, text='Username: ').pack()
        entry_user = Entry(root2)
        entry_user.pack()
        Button(root2, text='Start chatting', command=lambda: (self.add_chat(entry_user.get()), root2.destroy())).pack()
        root2.mainloop()

    def add_chat(self, username):
        request = {
            'type': 'add_chat',
            'username': username,
            'user_id': self.client.user_id
        }
        self.client.broadcast.send_data(request)
        response = self.client.broadcast.read_data()
        if response['status'] == 'ok':
            self.open_chat(response)

    def ask_user_data(self, user_id):
        request = {
            'type': 'get_user_data',
            'user_id': user_id
        }
        self.client.broadcast.send_data(request)
        response = self.client.broadcast.read_data()
        if response['status'] == 'ok':
            return response['name'], response['surname']

    def make_text_for_button(self, chat):
        if chat['sender_id'] != 0:
            if self.client.user_id == chat['sender_id']:
                sender = 'you:'
            else:
                sender = '{0} {1}:'.format(chat['name'], chat['surname'])
            return '{0} {1}\n {2} {3}'.format(chat['name'], chat['surname'], sender, chat['content'])
        else:
            return '{0} {1}'.format(chat['name'], chat['surname'])
