from typing import Optional, Union
import ast

import discord

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

    def add(self, guild_id: int, title: str, desc: str):
        data = {
            "guild_id": guild_id,
            "title": title,
            "description": desc,
        }
        self.insert(data)

    def get(self, guild_id: int = None) -> Optional[list]:
        """
        Возвращает настройки связи ролей-реакции в виде словаря

        :param guild_id: id сервера
        :return: Категории сервера
        """
        return self.select(where_expr=f"guild_id={guild_id}")


class ReactionRole(common.ExtendedDB):
    """
    Сообщения для выдачи ролей.
    """

    def __init__(self):
        super().__init__(Settings.Tables.REACTION_ROLES)

    def create_table(self):
        request = f"""CREATE TABLE IF NOT EXISTS {self.table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            role_id INTEGER,
            category_id INTEGER,
            emoji TEXT
        );"""
        self.execute_and_commit(request)

    def add(self, guild_id: int, role: discord.Role, emoji: str):
        params = {
            "guild_id": guild_id,
            "role_id": role.id,
            "emoji": emoji,
        }
        self.insert(params)

    def delete_msg(self, msg_id: int):
        self.delete("id", msg_id)

    def get_guild(self, guild_id: int) -> list:
        return self.select(where_expr=f"guild_id={guild_id}")

    def is_exist_msg(self, msg_id: int) -> bool:
        return bool(self.select(where_expr=f"id={msg_id}"))

    def get_msg_id(self, guild_id: int) -> Optional[list]:
        result = self.select(where_expr=f"guild_id={guild_id}")
        if result:
            return result[0][0]
        return None


def main():
    msg = ReactionRole()
    msg.create_table()
    role_setting = {
        "♥": 1073578706917929020,
        "😄": 1073579255432228955,
    }
    data = {
        "id": 456,
        "guild_id": 10456,
    }
    msg.add(data)


if __name__ == '__main__':
    main()
