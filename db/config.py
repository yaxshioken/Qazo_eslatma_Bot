import datetime
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DB:

    def __init__(self):
        self.db = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        self.db.autocommit = True

    def create_user_table(self):
        cursor = self.db.cursor()
        create_user_sql = """
                          create table IF NOT EXISTS users
                          (
                              id SERIAL PRIMARY KEY,
                              username VARCHAR(128) UNIQUE,
                              telegram_id BIGINT,
                              first_name VARCHAR(255),
                              roles VARCHAR (25) DEFAULT 'user'
                              ); """
        cursor.execute(create_user_sql)
        self.db.commit()
        cursor.close()

    def create_qazo_table(self):
        cursor = self.db.cursor()
        create_qazo_table_sql = """
        CREATE TABLE IF NOT EXISTS qazo_namozlar (
             id INTEGER PRIMARY KEY ,
             user_id INTEGER,
             namoz_vaqti TEXT,
             qazo_soni INTEGER DEFAULT 0,
             last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             FOREIGN KEY (user_id) REFERENCES users(id));"""
        cursor.execute(create_qazo_table_sql)
        self.db.commit()
        cursor.close()
    def create_faq_table(self):
        cursor = self.db.cursor()
        create_faq_table_sql = """
         CREATE TABLE IF NOT EXISTS faq (
             id INTEGER PRIMARY KEY,
             question TEXT,
             answer TEXT,
             video_url TEXT);"""
        cursor.execute(create_faq_table_sql)
        self.db.commit()
        cursor.close()

    def insert_user(self, username, telegram_id, first_name):
        cursor = self.db.cursor()
        insert_into_users = """
                            INSERT INTO users(username, telegram_id, first_name)
                            VALUES (%s, %s, %s);"""
        cursor.execute(insert_into_users, (username, telegram_id, first_name,))
        self.db.commit()
        cursor.close()

    def insert_client(self, name: str, company, created_at: datetime, end_date: datetime, phone_number: str,
                      masul_xodim):
        cursor = self.db.cursor()
        insert_client_sql = """
                            INSERT INTO clients(name, company, created_at, end_date, phone_number, masul_xodim)
                            VALUES (%s, %s, %s, %s, %s, %s);"""
        cursor.execute(insert_client_sql, (name, company, created_at, end_date, phone_number, masul_xodim))
        self.db.commit()
        cursor.close()

    def check_user_exist(self, telegram_id: int):
        cursor = self.db.cursor()
        data_sql = "SELECT telegram_id FROM users WHERE telegram_id = %s;"
        cursor.execute(data_sql, (telegram_id,))
        data = cursor.fetchone()
        cursor.close()
        return data is not None

    # def check_unique_phone_number(self, phone_number):
    #     cursor = self.db.cursor()
    #     unique_phone_number_sql = """SELECT phone_number
    #                                  FROM clients
    #                                  WHERE phone_number = %s;"""
    #     cursor.execute(unique_phone_number_sql, (phone_number,))
    #     data = cursor.fetchone()
    #     cursor.close()
    #     return data is not None
    #
    # def check_client_name_unique(self, name):
    #     cursor = self.db.cursor()
    #     unique_client_name_sql = """SELECT name
    #                                 FROM clients
    #                                 WHERE name = %s;"""
    #     cursor.execute(unique_client_name_sql, (name,))
    #     data = cursor.fetchone()
    #     cursor.close()
    #     return data is not None
    #
    # def check_phone_number_exists(self, phone_number):
    #     cursor = self.db.cursor()
    #     phone_number_exist_sql = """SELECT phone_number
    #                                 FROM clients
    #                                 WHERE phone_number = %s;"""
    #     cursor.execute(phone_number_exist_sql, (phone_number,))
    #     data = cursor.fetchone()
    #     cursor.close()
    #     return data is not None
    #
    # def update_date(self, phone_number, boshlanish_date, tugash_date):
    #     cursor = self.db.cursor()
    #     update_date_sql = """ UPDATE clients
    #                           SET created_at = %s,
    #                               end_date   = %s
    #                           WHERE phone_number = %s;"""
    #     cursor.execute(update_date_sql, (boshlanish_date, tugash_date, phone_number))
    #     self.db.commit()
    #     cursor.close()
    #
    # def get_mijoz(self, phone_number):
    #     cursor = self.db.cursor()
    #     get_mijoz_sql = """SELECT *
    #                        FROM clients
    #                        WHERE phone_number = %s;"""
    #     cursor.execute(get_mijoz_sql, (phone_number,))
    #     self.db.commit()
    #     data = cursor.fetchone()
    #     cursor.close()
    #     return data
    #
    # def update_admin(self, telegram_id):
    #     cursor = self.db.cursor()
    #     update_user_sql = """UPDATE users
    #                          SET roles = 'admin'
    #                          WHERE telegram_id = %s;"""
    #     cursor.execute(update_user_sql, (telegram_id,))
    #     updated_rows = cursor.rowcount
    #     self.db.commit()
    #     cursor.close()
    #     return updated_rows > 0
    #
    # def check_admin(self, telegram_id):
    #     cursor = self.db.cursor()
    #     check_user_is_admin_sql = """SELECT telegram_id
    #                                  FROM users
    #                                  WHERE roles = 'admin';"""
    #     cursor.execute(check_user_is_admin_sql)
    #
    #     data = cursor.fetchall()
    #     for admin in data:
    #         if admin[0] == telegram_id:
    #             return True
    #     return False
    #
    # def get_clients(self):
    #     cursor = self.db.cursor()
    #     get_all_clients_sql = """SELECT *
    #                              FROM clients;"""
    #     cursor.execute(get_all_clients_sql)
    #     data = cursor.fetchall()
    #     return data
    #
    # def get_active_clients(self):
    #     cursor = self.db.cursor()
    #     get_all_clients_sql = """
    #                           SELECT *
    #                           FROM clients
    #                           WHERE end_date >= %s; \
    #                           """
    #     today = datetime.date.today()
    #     cursor.execute(get_all_clients_sql, (today,))
    #     data = cursor.fetchall()
    #     return data
    # def get_all_admin(self):
    #     cursor = self.db.cursor()
    #     get_all_admins = "SELECT telegram_id FROM users WHERE roles = 'admin';"
    #     cursor.execute(get_all_admins)
    #     data = cursor.fetchall()
    #     cursor.close()
    #     return data


if __name__ == '__main__':
    db = DB()
    db.create_user_table()
    db.create_qazo_table()
    db.create_faq_table()
# import sqlite3
# import datetime
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
#
# class DB:
#     def __init__(self):
#         self.db = sqlite3.connect(os.getenv("DB_NAME", "qazo.db"))
#         self.db.row_factory = sqlite3.Row
#         self.db.isolation_level = None
#
#     def create_user_table(self):
#         cursor = self.db.cursor()
#         cursor.execute("""
#          CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE,
#             telegram_id INTEGER,
#             first_name TEXT,
#             roles TEXT DEFAULT 'user'
#         );""")
#
#     def create_qazo_table(self):
#         cursor = self.db.cursor()
#         cursor.execute("""
#        CREATE TABLE IF NOT EXISTS qazo_namozlar (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id INTEGER,
#         namoz_vaqti TEXT,
#         qazo_soni INTEGER DEFAULT 0,
#         last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         FOREIGN KEY (user_id) REFERENCES users(id));""")
#
#     def create_faq_table(self):
#         cursor = self.db.cursor()
#         cursor.execute("""
#         CREATE TABLE IF NOT EXISTS faq (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             question TEXT,
#             answer TEXT,
#             video_url TEXT);
#             """)
#
#     def check_user_exist(self, telegram_id):
#         cursor = self.db.cursor()
#         cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
#         data = cursor.fetchone()
#         return data
#
#     def create_user(self, username, telegram_id, first_name):
#         with self.db:
#             self.db.execute("""
#                 INSERT OR IGNORE INTO users (username, telegram_id, first_name)
#                 VALUES (?, ?, ?)
#             """, (username, telegram_id, first_name))
#
#     def create_qazo(self, user_id, namoz_vaqti, qazo_soni):
#         with self.db:
#             self.db.execute("""
#                 INSERT INTO qazo_namozlar (user_id, namoz_vaqti, qazo_soni)
#                 VALUES (?, ?, ?)
#             """, (user_id, namoz_vaqti, qazo_soni))
#
#
# if __name__ == "__main__":
#     db = DB()
#     db.create_user_table()
#     db.create_qazo_table()
#     db.create_faq_table()
