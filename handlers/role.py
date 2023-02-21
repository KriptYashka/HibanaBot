import discord

from models.db.role import ReactionRole


async def add_reaction_role(guild_id: int, role: discord.Role, emoji: str):
    """
    Обработчик создания новой роли для сервера
    """
    db = ReactionRole()
    db.add(guild_id, role, emoji)


def is_role_message(message_id: int) -> bool:
    """
    Является ли сообщение вида "реакция-роль".

    :param message_id: id сообщения
    :return: True или False
    """
    return ReactionRole().is_exist_msg(message_id)


def check_msg_delete(msg_id: int, guild_id: int):
    db = ReactionRole()
    if msg_id == db.get_msg_id(guild_id):
        db.delete("id", msg_id)
