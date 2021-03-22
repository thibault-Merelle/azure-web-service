import psycopg2
import os
from dotenv import load_dotenv
import sys
load_dotenv('/home/azureuser/Ansible/.env')

class DB:
    def __init__(self):
        self._dbcon = None

    def __enter__(self):
        try:
            self._dbcon = psycopg2.connect(
                host=os.environ['AZ_POSTGRES_HOST'],
                user=os.environ['AZ_POSTGRES_USER'],
                password=os.environ['AZ_POSTGRES_PASSWORD'],
                database=os.environ['AZ_POSTGRES_DATABASE'],
                port=os.environ['AZ_POSTGRES_PORT']
            )
            self._cursor = self._dbcon.cursor()
            return self
        except:
            raise

    def __exit__(self, exc_type, exc_val, traceback):
        self._dbcon.close()

    def del_table(self):
        self._cursor.execute('DROP TABLE IF EXISTS users')
        self._dbcon.commit()

    def set_table(self):
        self._cursor.execute('CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, names VARCHAR(100) NOT NULL, UNIQUE(names))')
        self._dbcon.commit()

    def test_insert(self):
        self._cursor.execute("INSERT INTO users (names) VALUES ('Martin');")
        self._cursor.execute("INSERT INTO users (names) VALUES ('John');")
        self._dbcon.commit()

    # def check_user(self, user):
    #     self._cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE names LIKE (%s));", (user))
    #     exist = self._cursor.fetchall()
    #     return exist

    def insert_user(self, user):
        try:
            self._cursor.execute("INSERT INTO users (names) VALUES (%s);", (user,))
            self._dbcon.commit()
            return True
        except:
            return False

    def get_users(self):
        self._cursor.execute('SELECT * from users;')
        users = self._cursor.fetchall()
        users.sort()
        return users #jsonify sur le app.py

    def get_max(self):
        self._cursor.execute("SELECT id from users ORDER BY id DESC LIMIT 1;")
        max_id = self._cursor.fetchall()
        return str(max_id[0])
