from tkinter import *
from tkinter.ttk import *

class AuthPage:
    def __init__(self, broadcast):
        self.broadcast = broadcast
        self.root = Tk()
        self.root.config(bg='gray22')
        self.root.title('Authentication Page')
        self.root.geometry("{0}x{1}+{2}+{3}".format(400, 400, int((self.root.winfo_screenwidth() - 400) / 2),
                                                    int((self.root.winfo_screenheight() - 600) / 2)))
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
        view.geometry("{0}x{1}+{2}+{3}".format(200, 200, int((view.winfo_screenwidth() - 400) / 2),
                                                    int((view.winfo_screenheight() - 600) / 2)))
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
