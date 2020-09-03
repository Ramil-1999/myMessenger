from tkinter import *
from tkinter.scrolledtext import *
import scrollableFrame


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

    def create_widgets(self):
        self.ask_chats()
        self.frame1 = Frame()

        frame_top = Frame(self.frame1)
        Button(frame_top, text='+', width=100, command=self.window_add_chat).pack()
        frame_top.pack(side='top')

        frame_main = scrollableFrame.ScrollableFrame(self.frame1, 0)

        for chat in self.chats:
            Button(frame_main.scrollable_frame, width='100', text='{0} {1}'.format(chat['name'], chat['surname']),
                   command=lambda n=chat: self.open_chat(n), height=3, anchor='w').pack(fill=X)
        frame_main.pack(fill=BOTH, expand=1)
        self.frame1.pack(expand=1, fill=BOTH)
        self.root.mainloop()

    def open_chat(self, chat):
        print(chat)
        chat_id = chat['chat_id']
        name = chat['name']
        surname = chat['surname']

        self.frame1.destroy()
        # верстка экрана чата
        frame2 = Frame(self.root)
        frame_top = Frame(frame2)
        Button(frame_top, text='<--', width=10, command=lambda: (frame2.destroy(), self.create_widgets()))\
            .pack(side='left')
        Label(frame_top, text='{0} {1}'.format(name, surname), width=90).pack(side='right')
        frame_top.pack(side='top')

        frame_mid = scrollableFrame.ScrollableFrame(frame2, 1)
        self.messages = self.ask_history(chat_id)
        for message in self.messages:
            if self.client.user_id == message['user_id']:
                Label(frame_mid.scrollable_frame, text=message['content'], anchor='e', width=50).pack()
            else:
                Label(frame_mid.scrollable_frame, text=message['content'], anchor='w', width=55).pack()
        frame_mid.pack(fill=BOTH, expand=1)

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
        datetime = None
        request = {
            'type': 'send_message',
            'chat_id': chat_id,
            'user_id': user_id,
            'content': content,
            'datetime': datetime
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

