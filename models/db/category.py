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


class CategoryMessage(common.ExtendedDB):
    """
    Сообщения для выдачи ролей.
    """

    def __init__(self):
        super().__init__(Settings.Tables.CATEGORY_MESSAGE)

    def create_table(self):
        request = f"""CREATE TABLE IF NOT EXISTS {self.table} (
            msg_id INTEGER,
            channel_id INTEGER,
            guild_id INTEGER,
            category TEXT,
            PRIMARY KEY("msg_id","channel_id","guild_id")
        );"""
        self.execute_and_commit(request)

    def add(self, msg_id: int, channel_id: int, guild_id: int, title: str):
        params = {
            "msg_id": msg_id,
            "channel_id": channel_id,
            "guild_id": guild_id,
            "category": title,
        }
        self.insert(params)

    def delete_msg(self, msg_id: int):
        self.delete({"msg_id": msg_id})

    def get_all_in_guild(self, guild_id: int) -> list:
        return self.select(where_expr=f"guild_id={guild_id}")

    def is_exist_msg(self, msg_id: int) -> bool:
        return bool(self.select(where_expr=f"msg_id={msg_id}"))
