class Settings:
    """
    Класс настроек для бота
    """

    PREFIX = "/"
    DB_NAME = "test.db"
    debug = True

    class Tables:
        """
        Названия таблиц в БД
        """
        REACTION_ROLES = "reaction_roles"
        CATEGORY_ROLES = "category_roles"
