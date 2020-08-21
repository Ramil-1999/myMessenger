from tkinter import *
from tkinter.ttk import *


class RegPage:
    def __init__(self, client):
        self.root = Tk()
        self.client = client
        self.status = False

    def create_widgets(self):
        self.root.geometry("{0}x{1}+{2}+{3}".format(200, 200, int((self.root.winfo_screenwidth() - 400) / 2),
                                                    int((self.root.winfo_screenheight() - 400) / 2)))
        self.root.title('Registration')
        frame = Frame(self.root)
        Label(frame, text="Enter your login:", padding=3).pack()
        self.name = Entry(frame)
        self.name.pack()
        Label(frame, text="Enter password:", padding=3).pack()
        self.password = Entry(frame, show='*')
        self.password.pack()
        Label(frame, text="Confirm password:", padding=3).pack()
        self.password2 = Entry(frame, show='*')
        self.password2.pack()
        self.label = Label(frame, foreground='red', padding=3)
        self.label.pack()
        Button(frame, text='Registration', command=self.send_data).pack()
        frame.pack(expand=1)

    def send_data(self):
        if len(self.password2.get()) >= 8:
            if self.password.get() == self.password2.get():
                data_dict = {
                    'type': 'reg',
                    'username': self.name.get(),
                    'hash': self.password.get()
                }
                if self.client.broadcast.send_data(data_dict):
                    self.recv()
            else:
                self.label['text'] = "!passwords don't match"
        else:
            self.label['text'] = "!password is too short"

    def recv(self):
        status = self.client.broadcast.read_data()
        if status['status'] == 'ok':
            self.root.destroy()
            print('from RegPage: status become true')
            self.status = True
        elif status['status'] == 'login':
            self.label.text = '!A user with this name already exists'

    @staticmethod
    def show(client):
        reg = RegPage(client)
        reg.create_widgets()
        print()
        reg.root.mainloop()
        return reg.status
