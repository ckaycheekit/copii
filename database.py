import sqlite3


class Database:
    def __init__(self):
        self.con = self.get_connection()
        self.login()

    def check_table_exists(self, table):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(table)
        if len(self.con.execute(query).fetchall()) == 0:
            return False
        else:
            return True

    def login(self):
        table = 'credentials'
        if not self.check_table_exists(table):
            self.create_table(table)

    # def create_account(self, username, passcode):
    #     self.insert_data('credentials', username=username, passcode=passcode)

    def get_connection(self):
        conn = sqlite3.connect('data.db')
        return conn

    def close_connection(self):
        self.con.close()

    def create_table(self, table):
        if table == 'secrets':
            query = "CREATE TABLE secrets (tag TEXT, secret TEXT)"
        elif table == 'credentials':
            query = "CREATE TABLE credentials (username TEXT, passcode TEXT)"
        self.con.execute(query)

    def get_all_tags(self, table):
        # Create table if not exists
        if not self.check_table_exists('secrets'):
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

    def get_username(self):
        query = "SELECT username from credentials"
        res = self.con.execute(query)
        for val in res:
            return val[0]

    def get_passcode(self, username):
        query = "SELECT passcode from credentials WHERE username = '{}'".format(username)
        res = self.con.execute(query)
        for val in res:
            return val[0]

    def insert_data(self, table, username=None, passcode=None, tag=None, secret=None):
        if table == 'secrets':
            query = "INSERT INTO '{}' (tag, secret) VALUES ('{}', '{}')".format(table, tag, secret)
        elif table == 'credentials':
            query = "INSERT INTO '{}' (username, passcode) VALUES ('{}', '{}')".format(table, username, passcode)
        self.con.execute(query)
        self.con.commit()

    def delete_data(self, tag):
        query = "DELETE FROM secrets WHERE tag = '{}'".format(tag)
        self.con.execute(query)
        self.con.commit()

