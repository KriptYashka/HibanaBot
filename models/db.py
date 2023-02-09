import sqlite3
from typing import List, Optional
import stat


class DB:
    """
    Базовый класс БД
    """

    @staticmethod
    def get_table_keys_and_values(params: dict[str, str]) -> tuple[str, str]:
        key_params = list(params.keys())
        value_params = list(params.values())
        table_keys = "(" + ",".join(key_params) + ")"
        table_values = "(" + ",".join(['null' if value == 'null' else f"\"{value}\"" for value in value_params]) + ")"
        return table_keys, table_values

    @staticmethod
    def get_insert_format(table: str, params: dict[str, str]):
        table_keys, table_values = DB.get_table_keys_and_values(params)
        request = f"INSERT INTO {table} {table_keys} VALUES {table_values};"
        return request

    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute_and_commit(self, request: str):
        """
        Выполняет запрос и фиксирует изменения в БД

        :param request: запрос к БД на языке SQLite3
        """
        print(request)
        self.cursor.execute(request)
        self.conn.commit()

    def select_item(self, table_name: str, where_params=None) -> List[str]:
        """
        Возвращает объекты из таблицы

        :param table_name: название таблицы
        :return: Список искомых объектов
        """
        request = f"SELECT * FROM {table_name}"
        if where_params is not None:
            request += " WHERE "
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def insert(self, table_name: str, params: dict[str, str]):
        """
        Добавляет в нужную таблицу данные ( data )

        :param table_name: название таблицы
        :param params: словарь данных объекта
        """
        request_insert = DB.get_insert_format(table_name, params)
        self.execute_and_commit(request_insert)

    def select(self, table_name, search_item_name=None, search_item_value=None):
        """
        Поиск объектов в таблице
        """
        request = "SELECT * FROM `{}`".format(table_name)
        if search_item_name is None:
            request += ";"
        else:
            request += " WHERE {} = {};".format(search_item_name, search_item_value)
        print(request)
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def delete(self, table_name, search_item_name=None, search_item_value=None):
        """
        Удаление объекта в таблице
        """
        request = f"DELETE FROM {table_name} WHERE {search_item_name} = {search_item_value}"
        self.execute_and_commit(request)

    def get_id(self, table_name):
        request = "SELECT * FROM {}".format(table_name)
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        arr = []
        for item in result:
            arr.append(item[0])
        return arr


def main():
    db = DB("test.db")


if __name__ == '__main__':
    main()
