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

    def fetch_one(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users")

            row = cursor.fetchone()

            return row

        except Error as e:
            print(e)

        cursor.close()