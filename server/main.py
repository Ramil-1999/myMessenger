import server


def main():
    serv = server.Server('127.0.0.1', 10001)
    print(serv.db.fetch_one())


if __name__ == '__main__':
    main()
