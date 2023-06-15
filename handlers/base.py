from models.db.common import ExtendedDB


class BaseHandler:
    """
    Обработчик запросов между интерфейсом и логикой. Следует использовать для косвеной работы с БД. \n
    Имеет обязательные методы.
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
        """
        Проверяет, существует ли объект в таблице.
        Все ключи объединятся оператором AND.
        """
        return bool(self.db.select(where_expr=" AND ".join([f"{key} = '{value}'" for key, value in data.items()])))

    def add(self, **kwargs):
        """
        Добавляет запись в БД по ключам.
        Информацию о ключах можно найти в классе БД сущности.
        """
        self.check_on_exist_kwargs(kwargs)
        self.db.insert(kwargs)

    def edit(self, where_expr: str = None, **kwargs):
        """
        Изменяет запись в БД по ключам.
        Информацию о ключах можно найти в классе БД сущности.
        """
        self.check_on_exist_kwargs(kwargs)
        self.db.update(kwargs, where_expr)

    def select(self, where_expr: str = None,
               column_expr: str = "*",
               order_by: str = None,
               is_desc: bool = False,
               is_distinct: bool = False,
               limit: int = 0,
               offset: int = 0) -> list:
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
        # TODO: Проверка на правильность введенных данных
        return self.db.select(where_expr, column_expr, order_by, is_desc, is_distinct, limit, offset)

    def delete(self, **kwargs) -> bool:
        """
        Удаляет объект по ключам.\n
        Все ключи объединятся оператором AND.

        :return: Находился объект в БД или нет.
        """
        if is_exist := self.is_exist_object(kwargs):
            self.db.delete(kwargs)
        return bool(is_exist)
