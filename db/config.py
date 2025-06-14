import datetime
import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

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
                          create table IF NOT EXISTS users(
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(128) UNIQUE,
                            telegram_id BIGINT UNIQUE,
                            first_name VARCHAR(255),
                            roles VARCHAR(25) DEFAULT 'user'); """
        cursor.execute(create_user_sql)
        self.db.commit()

    def create_qazo_table(self):
        cursor = self.db.cursor()
        create_qazo_table_sql = """
            CREATE TABLE IF NOT EXISTS qazo_namozlar (
            id SERIAL PRIMARY KEY,
            user_id BIGINT ,
            Bomdod INTEGER DEFAULT 0,
            Peshin INTEGER DEFAULT 0,
            Asr INTEGER DEFAULT 0,
            Shom INTEGER DEFAULT 0,
            Xufton INTEGER DEFAULT 0
            );
        """
        cursor.execute(create_qazo_table_sql)
        self.db.commit()


    def create_faq_table(self):
        cursor = self.db.cursor()
        create_faq_table_sql = """
                               CREATE TABLE IF NOT EXISTS faq
                               (
                                   id  SERIAL PRIMARY KEY,
                                   question TEXT,
                                   answer TEXT,
                                   video_url TEXT
                               );"""
        cursor.execute(create_faq_table_sql)
        self.db.commit()

    def create_null_qazo(self, user_id):
        cursor = self.db.cursor()
        sql = """
              INSERT INTO qazo_namozlar (user_id, Bomdod, Peshin, Asr, Shom, Xufton)
              VALUES (%s, 0, 0, 0, 0, 0)"""
        cursor.execute(sql, (user_id,))
        self.db.commit()

    def update_qazo(self, user_id, Bomdod, Peshin, Asr, Shom, Xufton):
        cursor = self.db.cursor()
        sql = """
              INSERT INTO qazo_namozlar (user_id, Bomdod, Peshin, Asr, Shom, Xufton)
              VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (user_id, Bomdod, Peshin, Asr, Shom, Xufton))
        self.db.commit()

    def insert_user(self, username, telegram_id, first_name):
        cursor = self.db.cursor()
        insert_into_users = """
                            INSERT INTO users (username, telegram_id, first_name)
                            VALUES (%s, %s,%s) ON CONFLICT (telegram_id) DO NOTHING; \
                            """
        cursor.execute(insert_into_users, (username, telegram_id, first_name))
        self.db.commit()

    def check_user_exist(self, telegram_id):
        cursor = self.db.cursor()
        data_sql = "SELECT telegram_id FROM users WHERE telegram_id = %s;"
        cursor.execute(data_sql, (telegram_id,))
        data = cursor.fetchone()
        return data is not None

    def get_all_qazos(self, telegram_id):
        cursor = self.db.cursor()
        get_all_qazos_sql = """
                            SELECT SUM(bomdod), SUM(peshin), SUM(asr), SUM(shom), SUM(xufton)
                            FROM qazo_namozlar
                            WHERE user_id = %s \
                            """
        cursor.execute(get_all_qazos_sql, (telegram_id,))
        data = cursor.fetchone()
        cursor.close()
        return {
            "bomdod": data[0] or 0,
            "peshin": data[1] or 0,
            "asr": data[2] or 0,
            "shom": data[3] or 0,
            "xufton": data[4] or 0
        }

    def update_single_qazo(self, user_id: int, namoz: str, value: int):
        cursor = self.db.cursor()
        sql = f"""UPDATE qazo_namozlar SET {namoz} = %s WHERE user_id = %s"""
        cursor.execute(sql, (value, user_id))
        self.db.commit()

    def search_faqs(self, query: str):
        with self.db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                        SELECT id, question
                        FROM faq
                        WHERE LOWER(question) LIKE %s LIMIT 10
                        """, (f"%{query.lower()}%",))
            return cur.fetchall()

    def get_faq_by_question(self, question: str):
        with self.db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                        SELECT *
                        FROM faq
                        WHERE question = %s LIMIT 1
                        """, (question,))
            return cur.fetchone()

    def get_all_faqs(self):
        with self.db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT question FROM faq")
            return cur.fetchall()

    def add_faq(self, question: str, answer_text: str = None, answer_video_file_id: str = None):
        with self.db.cursor() as cur:
            cur.execute("""
                        INSERT INTO faqs (question, answer_text, answer_video_file_id)
                        VALUES (%s, %s, %s)
                        """, (question, answer_text, answer_video_file_id))
    # def add_qazo(self, telegram_id, date, count):
    #     cursor = self.db.cursor()
    #     cursor.execute("INSERT INTO qazo (user_id, date, count) VALUES (?, ?, ?)",
    #                    (telegram_id, date, count))
    #     self.db.commit()
    #
    # def get_qazo(self, telegram_id):
    #     cursor = self.db.cursor()
    #     cursor.execute("SELECT SUM(count) FROM qazo WHERE user_id = ?", (telegram_id,))
    #     result = cursor.fetchone()
    #     return result[0] if result[0] else 0
    #
    # def get_pending_qazo(self, telegram_id):
    #     cursor = self.db.cursor()
    #     cursor.execute("SELECT date, count FROM qazo WHERE user_id = ? AND notified = 0", (telegram_id,))
    #     return cursor.fetchall()
    #
    # def mark_notified(self, telegram_id):
    #     cursor = self.db.cursor()
    #     cursor.execute("UPDATE qazo SET notified = 1 WHERE user_id = ?", (telegram_id,))
    #     self.db.commit()

    def get_all_users(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT telegram_id FROM users")
        return [row[0] for row in cursor.fetchall()]

    def drop_db(self):
        cursor = self.db.cursor()
        cursor.execute("drop table if exists public.qazo_namozlar cascade;"
                       "drop table if exists public.users cascade;"
                       "drop table if exists public.faq cascade;")


if __name__ == '__main__':
    db = DB()
    db.create_user_table()
    db.create_qazo_table()
    db.create_faq_table()
    # db.drop_db()
