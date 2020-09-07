from tkinter import *
from tkinter.scrolledtext import *
import scrollableFrame
import threading


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
        self.chats = self.client.ask_chats()
        self.frame1 = Frame(self.root, bg='gray25')

        frame_top = Frame(self.frame1, bg='gray25')
        Button(frame_top,
               text='+',
               width=100,
               bg='gray55',
               activebackground="gray25",
               activeforeground="#EAECEE",
               command=self.window_add_chat).pack()
        frame_top.pack(side='top', padx=10, pady=10)

        frame_main = scrollableFrame.ScrollableFrame(self.frame1, bg='gray25')

        # вывод всех доступных чатов
        for chat in self.chats:
            txt = self.make_text_for_button(chat)
            Button(frame_main.scrollable_frame,
                   width='90',
                   text=txt,
                   bg="#2C3E50",
                   fg="#EAECEE",
                   activebackground="#17202A",
                   font="Helvetica 12",
                   height=3,
                   anchor='w',
                   justify='left',
                   activeforeground="#EAECEE",
                   command=lambda n=chat: self.goHead(n)).pack()
        frame_main.pack(fill=BOTH, expand=1)
        self.frame1.pack(expand=1, fill=BOTH)
        self.root.mainloop()

    def goHead(self, chat):
        self.frame1.destroy()
        self.open_chat(chat)

        self.rcv = threading.Thread(target=self.receive, daemon=True)
        self.rcv.start()

    # создание страницы открытого чата
    def open_chat(self, chat):
        self.chat_id = chat['chat_id']
        self.name = chat['name']
        surname = chat['surname']

        # верстка экрана чата
        frame2 = Frame(self.root, bg='gray25')

        # шапка из кнопки возврата и имени пользователя на той стороне чата)
        frame_top = Frame(frame2, bg='gray25')
        Button(frame_top,
               text='<--',
               width=10,
               bg="gray55",
               activebackground='gray25',
               command=lambda: (frame2.destroy(), self.create_widgets())).pack(side='left')
        Label(frame_top,
              text='{0} {1}'.format(self.name, surname),
              width=90,
              font="Helvetica 13 bold",
              bg="gray55").pack(side='right')
        frame_top.pack(side='top', padx=10, pady=10)

        # фрейм в котором отображаются сообщения
        frame_mid = Frame(frame2)
        self.messages = self.client.ask_history(self.chat_id)
        self.chat_field = ScrolledText(frame_mid,
                                       bg="#17202A",
                                       fg="#EAECEE",
                                       font="Helvetica 12",
                                       padx=10,
                                       pady=10)
        self.chat_field.see(END)
        self.show_messages()
        self.chat_field.pack(fill=BOTH, expand=1)
        frame_mid.pack(fill=BOTH, padx=10)

        # фрейм-хвост
        frame_bottom = Frame(frame2, bg='gray25')
        self.text_field = Text(frame_bottom,
                               width=35,
                               bg="#2C3E50",
                               fg="#EAECEE")
        self.text_field.pack(side='left', padx=10, pady=10, fill=BOTH)
        Button(frame_bottom,
               command=lambda: (self.client.send_message(self.chat_id,
                                                         self.client.user_id,
                                                         self.text_field.get(1.0, END)),
                                self.text_field.delete(1.0, END)),
               text='Send',
               bg="gray55",
               font="Helvetica 10 bold",
               width=20,
               activebackground='gray25').pack(side='right', fill=BOTH, expand=1, padx=10, pady=10)
        frame_bottom.pack(side='bottom')
        frame2.pack(fill=BOTH, expand=1)

    def show_messages(self):
        self.chat_field.configure(state='normal')
        self.chat_field.delete(1.0, END)
        for message in self.messages:
            if self.client.user_id == message['user_id']:
                self.chat_field.insert(END, '{0}: {1}'.format('You', message['content']))
            else:
                self.chat_field.insert(END, '{0}: {1}'.format(self.name, message['content']))
        self.chat_field.configure(state='disabled')

    def receive(self):
        while True:
            try:
                new_history = self.client.ask_history(self.chat_id)
                if new_history != self.messages:
                    self.messages = new_history
                    self.show_messages()
            except:
                pass

    def window_add_chat(self):
        root2 = Toplevel()
        root2.title('Create New Chat')
        root2.geometry("{0}x{1}+{2}+{3}".format(200, 200, int((self.root.winfo_screenwidth() - 200) / 2),
                                                int((self.root.winfo_screenheight() - 200) / 2)))
        Label(root2, text='Username: ').pack()
        entry_user = Entry(root2)
        entry_user.pack()
        Button(root2, text='Start chatting', command=lambda: (self.new_chat(entry_user.get()), root2.destroy()))\
            .pack()
        root2.mainloop()

    def new_chat(self, username):
        result = self.client.add_chat(username)
        if result:
            self.goHead(result)

    def make_text_for_button(self, chat):
        if chat['sender_id'] != 0:
            if self.client.user_id == chat['sender_id']:
                sender = 'you:'
            else:
                sender = '{0} {1}:'.format(chat['name'], chat['surname'])
            content = chat['content'][:-1]
            if len(chat['content']) > 10:
                content = chat['content'][:10] + '...'
            return '{0} {1}\n{2} {3}'.format(chat['name'], chat['surname'], sender, content)
        else:
            return '{0} {1}'.format(chat['name'], chat['surname'])
