import datetime

import sqlite3


def test():
    sqlite_connection = sqlite3.connect("/home/goto/PycharmProjects/publishingCenter/publishing.sqlite")

    query = '''select * from users'''

    cursor = sqlite_connection.cursor()
    cursor.execute(query)

    # sqlite_connection.commit()g
    print(cursor.fetchall())

if __name__ == '__main__':
    test()