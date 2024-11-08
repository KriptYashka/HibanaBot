import sqlite3
from typing import List, Optional, Any, Union
import random

from settings import Settings


class DB:
    """
    Базовый класс базы данных.
    """

    @staticmethod
    def get_table_kwargs(params: dict[str, Any]) -> tuple[str, str]:
        """
        Разделяет словарь на строки ключей и значений

        :param params: данные объекта
        :return: строку колонок и строку значений, нормализованных под SQL-формат
        """
        col_params = list(params.keys())
        value_params = list(params.values())
        table_cols = "(" + ",".join(col_params) + ")"
        table_values = "(" + ",".join(
            ['null' if value == 'null' or value is None else f"\"{value}\"" for value in value_params]) + ")"
        return table_cols, table_values

    def __init__(self, table: str, db_name: str = Settings.DB_NAME):
        """
        Создает объект БД. Если БД не существует -- создает новую.

        :param db_name: название базы данных
        :param table: текущая таблица
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table = table

    def execute_and_commit(self, request: str):
        """
        Выполняет запрос и фиксирует изменения в БД.

        :param request: запрос к БД на языке SQLite3
        """
        if Settings.debug:
            print(request)
        self.cursor.execute(request)
        self.conn.commit()

    def select(self, where_expr: str = None,
               column_expr: str = "*",
               order_by: str = None,
               is_desc: bool = False,
               is_distinct: bool = False,
               limit: int = 0,
               offset: int = 0) -> List:
        """
        Возвращает объекты из таблицы.

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

        request += f"{column_expr} FROM {self.table}"

        if where_expr is not None:
            request += " WHERE " + where_expr

        if order_by is not None:
            request += f" ORDER BY {order_by}"
            if is_desc:
                request += " DESC"

        if limit:
            request += f" LIMIT {limit}"
            if offset:
                request += f" OFFSET {offset}"
        request += ";"
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def insert(self, params: dict):
        """
        Добавляет новый объект.

        :param params: словарь данных объекта
        """
        table_cols, table_values = DB.get_table_kwargs(params)
        request = f"INSERT INTO {self.table} {table_cols} VALUES {table_values};"
        self.execute_and_commit(request)

    def replace(self, params: dict):
        """
        Добавляет или изменяет данные объекта.

        :param params: словарь данных объекта
        """
        table_cols, table_values = DB.get_table_kwargs(params)
        request = f"REPLACE INTO {self.table} {table_cols} VALUES {table_values};"
        self.execute_and_commit(request)

    def update(self, params: dict, where_expr: str):
        """
        Добавляет в таблицу данные.

        :param params: Словарь данных объекта
        :param where_expr: Фильтр объектов
        """
        set_expression = ",".join([f"{key} = \"{value}\"" for key, value in params.items() if value is not None])
        set_expression = set_expression.replace('"NULL"', 'NULL')
        request = f"UPDATE {self.table} SET {set_expression} WHERE {where_expr};"
        self.execute_and_commit(request)

    def delete(self, where_dict: dict):
        """
        Удаление объекта из таблицы.

        :param where_dict: Словарь значений
        """
        where_request = " AND ".join([f"{key} = '{value}'" for key, value in where_dict.items()])
        request = f"DELETE FROM {self.table} WHERE {where_request};"
        self.execute_and_commit(request)

    def col_names(self) -> List[str]:
        """
        Возвращает названия колонок в таблице.
        """
        request = f"PRAGMA table_info('{self.table}');"
        self.execute_and_commit(request)
        response = self.cursor.fetchall()
        names = []
        for row in response:
            names.append(row[1])
        return names

    def get_count_rows(self, col_name: str = "*", where_expr: str = None) -> int:
        """
        Подсчитывает количество записей по критериям.
        """
        request = f"SELECT COUNT({col_name}) FROM {self.table}"
        if where_expr:
            request += " WHERE " + where_expr
        self.execute_and_commit(request)
        return self.cursor.fetchone()[0]


class ExtendedDB(DB):
    """
    Расширенный класс БД с часто используемыми методами. Используется для наследования.
    """

    def __init__(self, table: str):
        super().__init__(table)

    def create_table(self):
        """
        Создается таблица в БД с необходимыми полями.
        """
        pass

    def get_all(self, column_expr: str = None) -> list:
        """
        Возвращает все записи из таблицы.

        :param column_expr: Колонки для отображения
        """
        return self.select(column_expr)

    def insert_many(self, list_params: List[dict]):
        """
        Добавляет много записей в таблицу.
        """
        for params in list_params:
            self.insert(params)


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


if __name__ == '__main__':
    main()
