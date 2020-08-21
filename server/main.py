import server
import json


def main():
    serv = server.Server('127.0.0.1', 10001)
    conn, adr = serv.socket.accept()
    while True:
        message = json.loads(conn.recv(1024).decode())
        print(serv.auth(message))
        conn.send(json.dumps({'status': 'ok'}).encode())


if __name__ == '__main__':
    main()
