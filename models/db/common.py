import sqlite3
from typing import List, Optional, Any
import random

from settings import Settings


class DB:
    """
    Базовый класс базы данных
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
        Создает объект БД. Если его не существует, тогда создает файл

        :param db_name: название базы данных
        :param table: текущая таблица
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table = table

    def execute_and_commit(self, request: str):
        """
        Выполняет запрос и фиксирует изменения в БД

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
               offset: int = 0) -> Optional[list]:
        """
        Возвращает объекты из таблицы

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

        if limit != 0:
            request += f" LIMIT {limit}"
            if offset != 0:
                request += f" OFFSET {offset}"
        request += ";"
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def insert(self, params: dict[str, Any]):
        """
        Добавляет новый объект

        :param table_name: название таблицы
        :param params: словарь данных объекта
        """
        table_cols, table_values = DB.get_table_kwargs(params)
        request = f"INSERT INTO {self.table} {table_cols} VALUES {table_values};"
        self.execute_and_commit(request)

    def replace(self, params: dict[str]):
        """
        Добавляет или изменяет данные объекта

        :param table_name: название таблицы
        :param params: словарь данных объекта
        """
        table_cols, table_values = DB.get_table_kwargs(params)
        request = f"REPLACE INTO {self.table} {table_cols} VALUES {table_values};"
        self.execute_and_commit(request)

    def update(self, params: dict[str, Any], where_expr: str):
        """
        Добавляет в нужную таблицу данные

        :param table_name: название таблицы
        :param params: словарь новых данных объекта
        :param where_expr: фильтр объектов
        """
        set_expression = ",".join([f"{key} = \"{value}\"" for key, value in params.items() if value is not None])
        request = f"UPDATE {self.table} SET {set_expression} WHERE {where_expr};"
        self.execute_and_commit(request)

    def delete(self, column: str = None, value: Any = None):
        """
        Удаление объекта в таблице

        :param column: ключ, по которому мы ищем объект
        :param value: значение у ключа объекта, который нужно удалить
        """
        request = f"DELETE FROM {self.table} WHERE {column} = {value};"
        self.execute_and_commit(request)

    def col_names(self) -> List[str]:
        """
        Возвращает названия колонок в таблице
        """
        request = f"PRAGMA table_info('{self.table}');"
        names = []
        for row in request:
            names.append(row[1])
        return names



class ExtendedDB(DB):
    """
    Расширенный класс БД с часто используемыми методами. Используется для наследования.
    """

    def __init__(self, table: str):
        super().__init__(table)

    def create_table(self):
        pass

    def get_all(self, column_expr: str = None) -> list:
        return self.select(column_expr)

    def insert_many(self, list_params: List[dict[str, Any]]):
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
    item = db.select("my_table", where_expr="skill<2000", column_expr="name, skill")
    print(item)


if __name__ == '__main__':
    main()
