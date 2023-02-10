class Settings:
    """
    Класс настроек для бота
    """

    PREFIX = "!"
    DB_NAME = "test.db"
    debug = True

    class tables:
        """
        Названия таблиц в БД
        """
        MSG_ROLES = "msg_roles"
        MSG_ROLES_SETTINGS = "msg_roles_settings"
