# coding: utf-8

import MySQLdb

def getConnection(dbName):
    conn = MySQLdb.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'root',
            db = dbName
        )
    conn.set_character_set('utf8')
    return conn

if __name__ == '__main__':
    print getConnection()
