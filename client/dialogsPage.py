from tkinter import *


class DialogsPage:
    def __init__(self, client):
        self.client = client
        self.chats = []
        self.ask_chats()
        self.root = Tk()
        self.root.title('Dialogs')
        self.root.geometry("{0}x{1}+{2}+{3}".format(400, 600, int((self.root.winfo_screenwidth() - 400)/2),
                                                    int((self.root.winfo_screenheight() - 600)/2)))
        self.create_widgets()


    def create_widgets(self):
        self.frame1 = Frame()
        for chat in self.chats:
            Button(self.frame1, width='100', text=chat, command=lambda: self.open_chat(chat[0]), height=3, anchor='w').pack(fill=X)
            Button(self.frame1, width='100', text=chat, command=lambda: self.open_chat(chat[0]), height=3, anchor='w').pack(fill=X)
        self.frame1.pack()
        self.root.mainloop()

    def open_chat(self, chat_id):
        self.frame1.destroy()

        # верстка экрана чата
        frame2 = Frame(self.root)
        frame_top = Frame(frame2)
        Button(frame_top, text='<-', width=10, command=lambda: (frame2.destroy(), self.create_widgets()))\
            .pack(side='left')
        Label(frame_top, text='user_name', width=90).pack(side='right')
        frame_top.pack(side='top')

        frame_mid = Frame(frame2)
        Label(frame_mid, text='1 message', width=100, anchor='e').pack()
        Label(frame_mid, text='2 message', width=100, anchor='w').pack()
        frame_mid.pack()


        frame_bottom = Frame(frame2)
        Text(frame_bottom, width=45, height=2).pack(side='left')
        Button(frame_bottom, command=lambda: (), text='send').pack(side='right')
        frame_bottom.pack(side='bottom')
        frame2.pack(fill=Y, expand=1)

    def ask_chats(self):
        request = {
            'type': 'get_chats',
            'user_id': 2  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! HARD CODE
        }
        self.client.broadcast.send_data(request)
        self.chats = self.client.broadcast.read_data()
