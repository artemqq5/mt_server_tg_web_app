import pymysql
import pymysql.cursors

from config import DATABASE_PASSWORD, DATABASE_NAME


class DefaultDataBase:

    def __init__(self):
        self.__connection = pymysql.connect(
            host="localhost",
            user="root",
            password=DATABASE_PASSWORD,
            db=DATABASE_NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def _insert(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    return cursor.execute(query, args)
        except Exception as e:
            print(f"_insert: {e} | {query}")

    def _update(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    return cursor.execute(query, args)
        except Exception as e:
            print(f"_update: {e} | {query}")

    def _delete(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    return cursor.execute(query, args)
        except Exception as e:
            print(f"_delete: {e} | {query}")

    def _select_one(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    cursor.execute(query, args)
                    return cursor.fetchone()
        except Exception as e:
            print(f"_select_one: {e} | {query}")

    def _select(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    cursor.execute(query, args)
                    return cursor.fetchall()
        except Exception as e:
            print(f"_select_all: {e} | {query}")
