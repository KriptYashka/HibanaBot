from models.db.common import ExtendedDB


class BaseHandler:
    """
    Обработчик запросов между интерфейсом и логикой. Следует использовать для косвеной работы с БД. \n
    Имеет обязательные методы:
    :
    """
    def __init__(self, db: ExtendedDB):
        self.db = db

    def check_on_exist_kwargs(self, kwargs):
        """
        Проверяет соответствие словаря с названиями столбцов в БД

        :param kwargs: Словарь для передачи в запрос
        """
        col_names = self.db.col_names()
        for name in kwargs:
            if not (name in col_names):
                error_text = f"Свойства таблицы {self.db.table} не имеет {name}.\nДоступные колонки: {col_names}"
                raise Exception(error_text)

    def is_exist_object(self, data: dict):
        return bool(self.db.select(where_expr=" AND ".join([f"{key} = '{value}'" for key, value in data.items()])))

    def add(self, **kwargs):
        self.check_on_exist_kwargs(kwargs)
        self.db.insert(kwargs)

    def edit(self, where_expr: str = None, **kwargs):
        self.check_on_exist_kwargs(kwargs)
        self.db.update(kwargs, where_expr)

    def select(self, where_expr: str = None,
               column_expr: str = "*",
               order_by: str = None,
               is_desc: bool = False,
               is_distinct: bool = False,
               limit: int = 0,
               offset: int = 0) -> list:
        # TODO: Проверка на правильность введенных данных
        return self.db.select(where_expr, column_expr, order_by, is_desc, is_distinct, limit, offset)

    def delete(self, **kwargs) -> bool:
        if is_exist := self.db.select(where_expr=" AND ".join([f"{key} = '{value}'" for key, value in kwargs.items()])):
            self.db.delete(kwargs)
        return bool(is_exist)
