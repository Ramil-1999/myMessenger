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
        self.conn = MySQLConnection(**read_db_config())

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

    def reg_user(self, username, hash):
        query = "INSERT INTO users(id, username, hash) VALUES(%s,%s)"

        args = (username, hash)

        if self.find_user(username) == 0:

            cursor = self.conn.cursor()
            cursor.execute( query, args)
            if cursor.lastrowid:
                print('last insert id', cursor.lastrowid)
            else:
                print('last insert id not found')
            self.conn.commit()
            cursor.close()
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
                chats_dict.append({
                    'chat_id': chat[0],
                    'user_id': chat[2]})
            elif chat[2] == user_id:
                chats_dict.append({
                    'chat_id': chat[0],
                    'user_id': chat[1]})
        return chats_dict

    def get_history(self, chat_id):
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
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
        self.conn.commit()
        cursor.close()
        return 1
