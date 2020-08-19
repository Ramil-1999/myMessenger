import server
import json


def main():
    serv = server.Server('127.0.0.1', 10001)
    conn, adr = serv.socket.accept()
    while True:
        message = json.loads(conn.recv(1024).decode())
        print(serv.db.find_user(message['name']))


if __name__ == '__main__':
    main()
