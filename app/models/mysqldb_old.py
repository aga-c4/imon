'''
config = {
    'db':{    
        'host': '127.0.0.1',
        'port': 3309,
        'db': 'dbname',
        'user': 'dbuser',
        'passwd': 'dbpasswd'
    }
}
db = Mysqldb(config['db'])

# Выполнение запроса SELECT
result = db.query("SELECT * FROM users")
for row in result:
    print(row)

# Выполнение запроса INSERT
new_user_id = db.insert("INSERT INTO users (name, email) VALUES (%s, %s)", ("John Doe", "johndoe@example.com"))
print("New user ID:", new_user_id)

# Выполнение запроса UPDATE
updated_rows = db.update("UPDATE users SET email = %s WHERE id = %s", ("newemail@example.com", 1))
print("Updated rows:", updated_rows)

# Выполнение запроса DELETE
deleted_rows = db.delete("DELETE FROM users WHERE id = %s", (1,))
print("Deleted rows:", deleted_rows)
'''

import mysql.connector

from models.metasingleton import MetaSingleton

class Mysqldb_old(metaclass=MetaSingleton):
    connection = None

    def connect(self, config_db):
        if self.connection is None:
            self.connection = mysql.connector.connect(
                host=config_db['host'],
                port=config_db['port'],
                username=config_db['user'],
                password=config_db['passwd'],
                database=config_db['db']
            )
            self.cursor = self.connection.cursor()
        return self

    def query(self, sql, params=None, dictionary:bool=True):
        cursor = self.cursor
        if dictionary:
            cursor = self.connection.cursor(dictionary=True)

        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)   
        return cursor.fetchall()

    def insert(self, sql, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        self.connection.commit()
        return self.cursor.lastrowid

    def update(self, sql, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        self.connection.commit()
        return self.cursor.rowcount

    def delete(self, sql, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        self.connection.commit()
        return self.cursor.rowcount

    def __del__(self):
        pass
        # self.cursor.close()
        # self.connection.close()
