from tkinter import *


class RegPage:
    def __init__(self, client):
        self.root = Tk()
        self.root.resizable(width=FALSE, height=FALSE)
        self.client = client
        self.status = False

    def create_widgets(self):
        self.root.geometry("{0}x{1}+{2}+{3}".format(300, 500, int((self.root.winfo_screenwidth() - 300) / 2),
                                                    int((self.root.winfo_screenheight() - 500) / 2)))
        self.root.title('Registration')
        frame = Frame(self.root,
                      bg='gray25')
        frame_main = Frame(frame,
                           bg='gray55')
        frame_mid = Frame(frame_main,
                          bg='gray55')
        Label(frame_mid,
              text="Enter your login:",
              padx=5,
              bg='gray55',
              pady=5,
              font="Helvetica 11").pack()
        self.username = Entry(frame_mid,
                              bg='gray75',
                              font="Helvetica 11")
        self.username.pack()
        Label(frame_mid,
              text="Enter password:",
              bg='gray55',
              padx=5,
              pady=5,
              font="Helvetica 11").pack()
        self.password = Entry(frame_mid,
                              show='*',
                              bg='gray75',
                              font="Helvetica 11")
        self.password.pack()

        Label(frame_mid,
              bg='gray55',
              text="Confirm password:",
              padx=5,
              pady=5,
              font="Helvetica 11").pack()

        self.password2 = Entry(frame_mid,
                               show='*',
                               bg='gray75',
                               font="Helvetica 11")
        self.password2.pack()

        Label(frame_mid,
              text='Enter your name:',
              bg='gray55',
              padx=5,
              pady=5,
              font="Helvetica 11").pack()

        self.name = Entry(frame_mid,
                          bg='gray75',
                          font="Helvetica 11",)
        self.name.pack()

        Label(frame_mid,
              text='Enter your surname',
              bg='gray55',
              padx=5,
              pady=5,
              font="Helvetica 11").pack()

        self.surname = Entry(frame_mid,
                             bg='gray75',
                             font="Helvetica 11")
        self.surname.pack()

        self.label = Label(frame_mid,
                           foreground='snow',
                           bg='gray55',
                           font="Helvetica 10",
                           padx=5,
                           pady=5)
        self.label.pack()

        Button(frame_mid,
               text='Registration',
               command=self.send_data,
               font="Helvetica 11",
               bg="RoyalBlue4",
               activebackground='#2C3E50').pack()

        frame_mid.pack(expand=1)
        frame_main.pack(expand=1, fill=BOTH, padx=10, pady=10)
        frame.pack(expand=1, fill=BOTH)

    def send_data(self):
        if self.is_fields_empty():
            if len(self.password.get()) >= 0:
                if self.password.get() == self.password2.get():
                    data_dict = {
                        'type': 'reg',
                        'username': self.username.get(),
                        'hash': self.password.get(),
                        'name': self.name.get(),
                        'surname': self.surname.get()
                    }
                    if self.client.broadcast.send_data(data_dict):
                        self.recv()
                else:
                    self.label['text'] = "!passwords don't match"
            else:
                self.label['text'] = "!password is too short"
        else:
            self.label['text'] = '!please fill all fields'

    def recv(self):
        status = self.client.broadcast.read_data()
        if status['status'] == 'ok':
            self.root.destroy()
            self.status = True
        elif status['status'] == 'username':
            self.label['text'] = '!A user with this name already exists'

    @staticmethod
    def show(client):
        reg = RegPage(client)
        reg.create_widgets()
        reg.root.mainloop()
        return reg.status

    def is_fields_empty(self):
        if self.username.get() != '' and self.password.get() != "" \
                and self.name.get() != '' and self.surname.get() != '':
            return 1
        return 0
