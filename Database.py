import sqlite3


class Database:
    def __init__(self):
        self.db = sqlite3.connect('database.db')
        self.cursor = self.db.cursor()

    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            email TEXT,
            address TEXT
        )
        """
        self.cursor.execute(sql)
        self.db.commit()

    def insert(self, table, data):
        keys = ','.join(data.keys())
        values = ','.join(['?'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        return self.cursor.lastrowid

    def update(self, table, data, id):
        values = ','.join(['{key}=?'.format(key=key) for key in data])
        sql = 'UPDATE {table} SET {values} WHERE id=?'.format(table=table, values=values)
        try:
            self.cursor.execute(sql, tuple(data.values()) + (id,))
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    def delete(self, table, id):
        sql = 'DELETE FROM {table} WHERE id=?'.format(table=table)
        try:
            self.cursor.execute(sql, (id,))
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

        return self.cursor.rowcount

    def select(self, table):
        sql = 'SELECT * FROM {table}'.format(table=table)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def select_by_id(self, table, id):
        sql = 'SELECT * FROM {table} WHERE id=?'.format(table=table)
        self.cursor.execute(sql, (id,))
        return self.cursor.fetchone()

    def __del__(self):
        self.db.close()


obj = Database()
# obj.create_table()
users = {"name": "gita", "age": 20, "email": "gita@gmai.com", 'address': 'USA'}

res = obj.select_by_id('user', 1)
print(res)
