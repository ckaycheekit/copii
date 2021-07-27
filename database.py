import sqlite3


class Database:
    def __init__(self):
        self.con = self.get_connection()

    def get_connection(self):
        conn = sqlite3.connect('data.db')
        return conn

    def close_connection(self):
        self.con.close()

    def create_table(self):
        query = "CREATE TABLE secrets (tag TEXT, secret TEXT)"
        self.con.execute(query)

    def get_all_tags(self, table):
        # Create table if not exists
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(table)
        if len(self.con.execute(query).fetchall()) == 0:
            self.create_table()
        get_query = "SELECT * FROM secrets"
        # return self.con.execute(get_query)
        res = self.con.execute(get_query)
        for row in res:
            print(row[0])

    def get_secret(self, tag):
        query = "SELECT secret from secrets WHERE tag = '{}'".format(tag)
        res = self.con.execute(query)
        for val in res:
            print(val[0])

    def insert_data(self, tag, secret):
        query = "INSERT INTO secrets (tag, secret) VALUES ('{}', '{}')".format(tag, secret)
        self.con.execute(query)
        self.con.commit()

    def delete_data(self, tag):
        query = "DELETE FROM secrets WHERE tag = '{}'".format(tag)
        self.con.execute(query)
        self.con.commit()

