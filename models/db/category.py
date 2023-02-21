from typing import Optional

from models.db import common
from settings import Settings


class CategoryRole(common.ExtendedDB):
    """
    Совокупность ролей для определенной ситуации.
    """

    def __init__(self):
        super().__init__(Settings.Tables.CATEGORY_ROLES)

    def create_table(self):
        request = f"""CREATE TABLE IF NOT EXISTS {self.table} (
            guild_id INTEGER,
            title TEXT,
            description TEXT,
            mutually_exclusive BOOL,
            PRIMARY KEY(guild_id, title)
        );"""
        self.execute_and_commit(request)