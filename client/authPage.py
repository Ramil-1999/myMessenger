from regPage import *


class AuthPage:
    def __init__(self, client):
        self.client = client
        self.root = Tk()
        self.root.resizable(width=FALSE, height=FALSE)
        self.status = 0

    def create_widgets(self):
        self.root.title('Authentication Page')
        self.root.geometry("{0}x{1}+{2}+{3}".format(400, 400, int((self.root.winfo_screenwidth() - 400) / 2),
                                                    int((self.root.winfo_screenheight() - 400) / 2)))
        frame_main = Frame(self.root,
                           bg='gray25')
        frame_main2 = Frame(frame_main,
                            bg='gray55')
        frame1 = Frame(frame_main2,
                       bg='gray55')
        Label(frame1,
              text="Enter your login:",
              padx=5,
              pady=5,
              font="Helvetica 11",
              bg='gray55').pack()
        self.name = Entry(frame1,
                          bg="gray75",
                          font="Helvetica 11")
        self.name.pack()
        Label(frame1,
              text="Enter password:",
              padx=5,
              pady=5,
              font="Helvetica 11",
              bg='gray55').pack()
        self.password = Entry(frame1,
                              show='*',
                              bg="gray75",
                              font="Helvetica 11")

        self.password.pack()
        self.label = Label(frame1,
                           foreground='snow',
                           padx=5,
                           pady=5,
                           font="Helvetica 10",
                           bg="gray55")
        self.label.pack()
        frame2 = Frame(frame1, bg='gray25')
        Button(frame2,
               text='Enter',
               font="Helvetica 11",
               bg="gray75",
               activebackground='gray55',
               command=self.send_data).pack(side='left')
        Button(frame2,
               text='Registration',
               font="Helvetica 11",
               bg="RoyalBlue4",
               activebackground='#2C3E50',
               fg="#EAECEE",
               command=self.register).pack(side='left')
        frame2.pack()
        frame1.pack(expand=1)
        frame_main2.pack(fill=BOTH, expand=1, padx=10, pady=10)
        frame_main.pack(fill=BOTH, expand=1)

    @staticmethod
    def create_attention(attention):
        view = Tk()
        view.geometry("{0}x{1}+{2}+{3}".format(200, 200, int((view.winfo_screenwidth() - 200) / 2),
                                               int((view.winfo_screenheight() - 200) / 2)))
        view.title("Error")
        Label(view, text=f"Attention: {attention}").pack()
        Button(view, text='OK', command=view.destroy).pack(side='bottom')
        view.mainloop()

    def send_data(self):
        if self.is_fields_empty():
            data_dict = {
                'type': 'auth',
                'username': self.name.get(),
                'hash': self.password.get()
                }
            if self.client.broadcast.send_data(data_dict):
                self.recv()
                return 1
            else:
                self.client.logger.logging('Error of auth: Check something')
                AuthPage.create_attention("Check something")
        else:
            self.label['text'] = '!please fill all fields'

    def recv(self):
        status = self.client.broadcast.read_data()
        if status['status'] == 'ok':
            self.client.username = self.name.get()
            self.root.destroy()
            self.status = 1
            self.client.user_id = status['user_id']
        elif status['status'] == 'password':
            self.label['text'] = '!wrong password'
        elif status['status'] == 'username':
            self.label['text'] = '!username not registered'

    def register(self):
        self.root.destroy()
        self.status = 2

    @staticmethod
    def show(client):
        auth = AuthPage(client)
        auth.create_widgets()
        auth.root.mainloop()
        return auth.status

    def is_fields_empty(self):
        if self.name.get() != '' and self.password.get() != '':
            return 1
        return 0
