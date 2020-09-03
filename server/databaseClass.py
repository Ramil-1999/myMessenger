from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser


def read_db_config(filename='config.ini', section='mysql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


class Db:
    def __init__(self):
        self.db_config = read_db_config()
        self.conn = MySQLConnection(**self.db_config)

    def find_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")

        result = cursor.fetchall()
        for key in result:
            if key[1] == username:
                cursor.close()
                return key[2], key[0]
        cursor.close()
        return 0, 0

    def reg_user(self, username, hash, name, surname):
        query = "INSERT INTO users(username, hash) VALUES(%s,%s)"
        args = (username, hash)

        res, _ = self.find_user(username)
        if res == 0:

            cursor = self.conn.cursor()
            cursor.execute(query, args)
            self.conn.commit()
            cursor.close()
            user_id = self.get_user_id(username)
            if self.add_user_data(user_id, name, surname):
                return 1
        else:
            return 0

    def get_chats(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM chats")

        result = cursor.fetchall()
        chats_dict = []
        for chat in result:
            if chat[1] == user_id:
                name, surname = self.get_user_data(chat[2])
                chats_dict.append({
                    'chat_id': chat[0],
                    'user_id': chat[2],
                    'name': name,
                    'surname': surname
                })
            elif chat[2] == user_id:
                name, surname = self.get_user_data(chat[1])
                chats_dict.append({
                    'chat_id': chat[0],
                    'user_id': chat[1],
                    'name': name,
                    'surname': surname
                })
        return chats_dict

    def get_history(self, chat_id):
        self.conn.close()
        self.conn = MySQLConnection(**self.db_config)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM messages")

        result = cursor.fetchall()
        mess_dict = []
        for mess in result:
            if mess[1] == chat_id:
                mess_dict.append({
                    'user_id': mess[2],
                    'content': mess[3]
                    })
        return mess_dict

    def send_message(self, chat_id, user_id, content, datetime):
        query = "INSERT INTO messages(chat_id, user_id, content, time) VALUES(%s, %s, %s, %s)"

        args = (chat_id, user_id, content, datetime)

        cursor = self.conn.cursor()
        cursor.execute(query, args)

        self.conn.commit()
        cursor.close()
        return 1

    def add_chat(self, username, user_id):
        query = "INSERT INTO chats(f_user_id, s_user_id) VALUES(%s, %s)"

        s_user_id = self.get_user_id(username)

        if s_user_id:
            args = (user_id, s_user_id)
            name, surname =  self.get_user_data(user_id)
            cursor = self.conn.cursor()
            cursor.execute(query, args)
            self.conn.commit()
            cursor.close()
            return cursor.lastrowid, name, surname
        else:
            return 0

    def get_user_id(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")

        result = cursor.fetchall()
        for key in result:
            if key[1] == username:
                cursor.close()
                return key[0]
        cursor.close()
        return 0

    def add_user_data(self, user_id, name, surname):
        query = "INSERT INTO user_data(user_id, name, surname) VALUES(%s, %s, %s)"

        args = (user_id, name, surname)

        cursor = self.conn.cursor()
        cursor.execute(query, args)
        self.conn.commit()
        cursor.close()
        return 1

    def get_user_data(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user_data")

        result = cursor.fetchall()
        for key in result:
            if key[0] == user_id:
                cursor.close()
                return key[1], key[2]
        cursor.close()
        return 0
