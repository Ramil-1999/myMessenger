from tkinter import *
import socket


def isEmpty():
    pass


def create_sock(host, port):
    return socket.create_connection((host, port))


def send_info():
    temp = name.get() + password.get()
    print(name.get(), password.get())
    sock.sendall(temp.encode())


sock = create_sock('127.0.0.1', 10001)
root = Tk()
root.title('Main page')
root.geometry('400x400')
label1 = Label(text="name")
label2 = Label(text="password")
name = Entry()
password = Entry(show='*')
button1 = Button(text='Connect', bg='white', command=send_info)
label1.pack()
name.pack()
label2.pack()
password.pack()
button1.pack()
root.mainloop()


