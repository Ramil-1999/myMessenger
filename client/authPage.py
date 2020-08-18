from tkinter import *


class AuthPage:
    def __init__(self, broadcast):
        self.broadcast = broadcast
        self.root = Tk()
        self.root.title('Authentication Page')
        self.root.geometry('400x400')
        self.label1 = Label(text="name").pack()
        self.name = Entry()
        self.name.pack()
        self.label2 = Label(text="password").pack()
        self.password = Entry(show='*')
        self.password.pack()
        self.button1 = Button(text='Connect', command=self.send_info).pack()
        self.root.mainloop()

    @staticmethod
    def create_attention(attention):
        view = Tk()
        view.geometry('200x200+220+220')
        view.title("Error")
        label = Label(view, text=f"Attention: {attention}").pack()
        button = Button(view, text='OK', command=view.destroy).pack(side='bottom')
        view.mainloop()

    def send_info(self):
        tmp = self.name.get() + ' ' + self.password.get()
        if self.broadcast.send_info(tmp):
            self.root.destroy()
        else:
            AuthPage.create_attention("Check something")
