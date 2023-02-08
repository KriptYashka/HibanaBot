import sqlite3
from typing import List
import stat


class DB:
    """
    Базовый класс БД
    """

    @staticmethod
    def get_table_form(params):
        if params == "":
            return ""
        text = "("
        for item in params:
            text += item + ","
        text = text[:-1] + ")"
        return text

    @staticmethod
    def get_insert_format(table, params, table_params):
        req = "INSERT INTO {} {} VALUES (".format(table, DB.get_table_form(table_params))
        for item in params:
            if item == 'null':
                req += '{},'.format(item)
            else:
                req += '"{}",'.format(item)
        req = req[:-1] + ");"
        print(req)
        return req

    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def select_item(self, table, id=None):
        request = "SELECT * FROM {}".format(table)
        if id is not None:
            request += " WHERE id == {};".format(id)
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def execute_and_commit(self, request):
        """ Выполняет запрос и фиксирует изменения в БД """
        print(request)
        self.cursor.execute(request)
        self.conn.commit()

    def insert(self, table: str, data: List[str], col_fields=""):
        """
        Добавляет в нужную таблицу данные ( data )
        table - название таблицы в БД
        data - данные нового объекта
        col_fields - названия колонок таблицы БД. Если данные вводятся по порядку названия таблицы, этот параметр не
        требуется
        """
        request_insert = DB.get_insert_format(table, data, col_fields)
        self.execute_and_commit(request_insert)

    def select(self, table, search_item_name=None, search_item_value=None):
        """ Поиск объектов в таблице """
        request = "SELECT * FROM `{}`".format(table)
        if search_item_name is None:
            request += ";"
        else:
            request += " WHERE {} = {};".format(search_item_name, search_item_value)
        print(request)
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def delete(self, table, search_item_name=None, search_item_value=None):
        """ Удаление объекта в таблице """
        request = "DELETE FROM {} WHERE {} = {}".format(table, search_item_name, search_item_value)
        self.execute_and_commit(request)

    def get_id(self, table):
        request = "SELECT * FROM {}".format(table)
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        arr = []
        for item in result:
            arr.append(item[0])
        return arr
