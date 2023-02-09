import sqlite3
from typing import List, Optional
import random


class DB:
    """
    Базовый класс базы данных
    """

    @staticmethod
    def get_table_keys_and_values(params: dict[str]) -> tuple[str, str]:
        key_params = list(params.keys())
        value_params = list(params.values())
        table_keys = "(" + ",".join(key_params) + ")"
        table_values = "(" + ",".join(['null' if value == 'null' or value is None else f"\"{value}\"" for value in value_params]) + ")"
        return table_keys, table_values

    def __init__(self, db_name: str, debug=False):
        """
        Создает объект БД. Если его не существует, тогда создает файл

        :param db_name: название базы данных
        :param debug: режим отладки
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.debug = debug

    def execute_and_commit(self, request: str):
        """
        Выполняет запрос и фиксирует изменения в БД

        :param request: запрос к БД на языке SQLite3
        """
        if self.debug:
            print(request)
        try:
            self.cursor.execute(request)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print("Неверный SQL запрос:", e)
            print(request)

    def select(self, table_name: str, where_expr=None, column_expr="*", order_by=None, is_desc=False,
               is_distinct=False, limit=0, offset=0) -> list:
        """
        Возвращает объекты из таблицы

        :param table_name: название таблицы
        :param where_expr: фильтр для объектов
        :param column_expr: возвращаемые колонки у объекта
        :param order_by: колонка, по которой будет идти сортировка
        :param is_desc: если флаг True, то сортировка идет по убыванию
        :param is_distinct: если флаг True, то будет возвращать уникальные поля
        :param limit: количество элементов
        :param offset: смещение, относительно первых limit элементов
        :return: Список искомых объектов
        """
        request = f"SELECT "
        if is_distinct:
            request += "DISTINCT "

        request += f"{column_expr} FROM {table_name}"

        if where_expr is not None:
            request += " WHERE " + where_expr

        if order_by is not None:
            request += f" ORDER BY {order_by}"
            if is_desc:
                request += " DESC"

        if limit != 0:
            request += f" LIMIT {limit}"
            if offset != 0:
                request += f" OFFSET {offset}"
        request += ";"
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def insert(self, table_name: str, params: dict[str]):
        """
        Добавляет в нужную таблицу данные

        :param table_name: название таблицы
        :param params: словарь данных объекта
        """
        table_keys, table_values = DB.get_table_keys_and_values(params)
        request = f"INSERT INTO {table_name} {table_keys} VALUES {table_values};"
        self.execute_and_commit(request)

    def update(self, table_name: str, params: dict[str], where_expr: str):
        """
        Добавляет в нужную таблицу данные

        :param table_name: название таблицы
        :param params: словарь новых данных объекта
        :param where_expr: фильтр объектов
        """
        set_expression = ",".join([f"{key} = \"{value}\"" for key, value in params.items()])
        request = f"UPDATE {table_name} SET {set_expression} WHERE {where_expr};"
        self.execute_and_commit(request)

    def delete(self, table_name: str, column=None, value=None):
        """
        Удаление объекта в таблице

        :param table_name: название таблицы
        :param column: ключ, по которому мы ищем объект
        :param value: значение у ключа объекта, который нужно удалить
        """
        request = f"DELETE FROM {table_name} WHERE {column} = {value}"
        self.execute_and_commit(request)


def main():
    db = DB("test.db")
    create_table_request = f"""CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        skill INTEGER
    );"""
    db.execute_and_commit(create_table_request)
    data = {
        "skill": random.randint(1000, 9999)
    }
    db.delete("my_table", "id", 5)
    item = db.select("my_table", where_expr="skill<2000", column_expr="name, skill")
    print(item)


if __name__ == '__main__':
    main()
