class Settings:
    """
    Класс настроек для бота
    """

    PREFIX = "/"
    DB_NAME = "test.db"
    debug = True
    LIMIT_CATEGORY_COUNT = 5

    class Tables:
        """
        Названия таблиц в БД
        """
        REACTION_ROLES = "reaction_roles"
        CATEGORY_ROLES = "category_roles"
        CATEGORY_MESSAGE = "category_msg"
