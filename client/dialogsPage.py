from tkinter import *


class DialogsPage:
    def __init__(self, broadcast):
        self.broadcast = broadcast
        self.ask_chats()
        self.root = Tk()
        self.root.title('Dialogs')
        self.root.geometry("{0}x{1}+{2}+{3}".format(400, 600, int((self.root.winfo_screenwidth() - 400)/2),
                                                    int((self.root.winfo_screenheight() - 600)/2)))
        button1 = Button(width='100', text="Dialog-1").pack(fill=X)
        button2 = Button(width='100', text="Dialog-3").pack(fill=X)
        button3 = Button(width='100', text="Dialog-2").pack(fill=X)
        # button2 = Button(justify='left', width='100', text='Dialog-2', pady='10').pack(fill=X)
        # button3 = Button(text='Dialog-3', fg="#eee", bg="#333", pady='10').pack(fill=X)
        self.root.mainloop()

    def create_widgets(self):
        pass

    def ask_chats(self):
        pass

