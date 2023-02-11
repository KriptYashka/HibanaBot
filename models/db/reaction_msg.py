from typing import Optional, Union
import ast

import discord

from models.db import common
from settings import Settings


class SettingRole(common.ExtendedDB):
    """
    Реакции и роли, которые должны выдаваться
    """

    def __init__(self):
        super().__init__(Settings.Tables.MSG_ROLES_SETTINGS)

    def create_table(self):
        request = f"""CREATE TABLE IF NOT EXISTS {self.table} (
            guild_id INTEGER,
            role_settings TEXT NOT NULL,
            PRIMARY KEY (guild_id)
        );"""
        self.execute_and_commit(request)

    def add(self, guild_id: int, role_settings: dict[Union[str, discord.Emoji, int], int]):
        data = {
            "guild_id": guild_id,
            "role_settings": role_settings,
        }
        self.replace(data)

    def get(self, guild_id: int) -> Optional[dict[str, int]]:
        """
        Возвращает настройки связи ролей-реакции в виде словаря

        :param guild_id: id сервера
        :return: Словарь настроек связи ролей-реакции
        """
        item = self.select(where_expr=f"guild_id={guild_id}")
        if not item:
            return None
        settings_str = ast.literal_eval(item[0][1])  # TODO: Выяснить, как работает эта функция
        return settings_str


class MessageReaction(common.ExtendedDB):
    """
    Сообщения для выдачи ролей.
    """

    def __init__(self):
        super().__init__(Settings.Tables.MSG_ROLES)

    def create_table(self):
        request = f"""CREATE TABLE IF NOT EXISTS {self.table} (
            id INTEGER,
            guild_id INTEGER,
            PRIMARY KEY (id, guild_id)
        );"""
        self.execute_and_commit(request)

    def add(self, data: Union[dict[str, int], discord.Message], *args):
        params = data
        if isinstance(data, discord.Message):
            params = {
                "id": data.id,
                "guild_id": data.guild.id,
            }
        settings = SettingRole().get(params["guild_id"])
        if settings:
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
    msg = MessageReaction()
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
