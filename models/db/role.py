from typing import Optional

import discord

from models.db import common
from settings import Settings


class ReactionRole(common.ExtendedDB):
    """
    Роли с соответствующими реакциями
    """

    def __init__(self):
        super().__init__(Settings.Tables.REACTION_ROLES)

    def create_table(self):
        request = f"""CREATE TABLE IF NOT EXISTS {self.table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            role_id INTEGER,
            category TEXT,
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
        self.delete({"id": msg_id})


def main():
    pass


if __name__ == '__main__':
    main()
