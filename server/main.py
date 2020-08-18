import server


def main():
    serv = server.Server('127.0.0.1', 10001)
    conn, adr = serv.socket.accept()

    while True:
        message = conn.recv(1024)
        print(message.decode())
        if not message:
            conn.close()


if __name__ == '__main__':
    main()
