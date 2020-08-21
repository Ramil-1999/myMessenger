from regPage import *


class AuthPage:
    def __init__(self, client):
        self.client = client
        self.root = Tk()
        self.status = False

    def create_widgets(self):
        self.root.title('Authentication Page')
        self.root.geometry("{0}x{1}+{2}+{3}".format(400, 400, int((self.root.winfo_screenwidth() - 400) / 2),
                                                    int((self.root.winfo_screenheight() - 400) / 2)))
        Style().configure("TButton", padding=3, relief="flat", background="#ccc")
        frame1 = Frame()
        Label(frame1, text="Enter your login:", padding=3).pack()
        self.name = Entry(frame1)
        self.name.pack()
        Label(frame1, text="Enter password:", padding=3).pack()
        self.password = Entry(frame1, show='*')
        self.password.pack()
        self.label = Label(frame1, foreground='red', padding=3)
        self.label.pack()
        frame2 = Frame(frame1)
        Button(frame2, text='Enter', command=self.send_data, style="TButton").pack(side='left')
        Button(frame2, text='Registration', command=self.register, style="TButton").pack(side='left')
        frame2.pack()
        frame1.pack(expand=1)

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

    def recv(self):
        status = self.client.broadcast.read_data()
        if status['status'] == 'ok':
            self.root.destroy()
            self.status = True
        elif status['status'] == 'password':
            self.label['text'] = '!wrong password'
        elif status['status'] == 'login':
            self.label.text = '!username not registered'

    def register(self):
        reg = RegPage.show(self.client)

    @staticmethod
    def show(client):
        auth = AuthPage(client)
        auth.create_widgets()
        auth.root.mainloop()
        return auth.status


