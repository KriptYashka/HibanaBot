import discord

from models.db import common
from settings import Settings


class MessageReaction(common.ExtendedDB):
    """
    Сообщения для выдачи ролей.
    """

    def __init__(self):
        super().__init__(Settings.DB_NAME)

    def create_table(self):
        request = f"""CREATE TABLE IF NOT EXISTS {Settings.tables.MSG_ROLES} (
            id INTEGER,
            guild_id INTEGER,
            role_setting TEXT NOT NULL,
            PRIMARY KEY (id, guild_id)
        );"""
        self.execute_and_commit(request)

    def add(self, msg: discord.Message, role_settings: dict[str, int]):


def main():
    msg = MessageReaction()
    msg.create_table()
    role_setting = {
        "duck": 1073578706917929020,
        "cat": 1073579255432228955,
    }

    msg.add()


if __name__ == '__main__':
    main()
