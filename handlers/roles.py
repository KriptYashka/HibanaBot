import discord
from discord.ext import commands

from interactions.setting_role import SettingRoleView
from models.db.roles import ReactionRole, CategoryRole


async def add_reaction_role(interaction: discord.Interaction, role: discord.Role, emoji: str):
    """
    Обработчик создания новой роли для сервера
    """
    db = ReactionRole()
    db.add(interaction, role, emoji)


async def add_category(interaction: discord.Interaction, title: str, description: str = None):
    """
    Обработчик создания новой категории ролей
    """
    db = CategoryRole()
    db.add(interaction.guild_id, title, description)


async def send_msg_roles(msg: discord.Message, setting: dict[str, int], text: str = None) -> discord.Message:
    """
    Отправляет сообщение с реакциями-ролями.

    :param text: текст сообщения с реакциями-ролями
    :param msg: сообщение-запрос от пользователя
    :param setting: настройки сервера реакции-роли
    :return: отправленное сообщение о статусе операции
    """
    text = text if text else "Give roles"
    new_msg = await msg.channel.send(text)
    if new_msg:
        ReactionRole().add(new_msg)
        for emoji in setting:
            await new_msg.add_reaction(emoji)
    return new_msg


def is_role_message(message_id: int) -> bool:
    """
    Является ли сообщение вида "реакция-роль".

    :param message_id: id сообщения
    :return: True или False
    """
    return ReactionRole().is_exist_msg(message_id)


def get_setting_roles(guild_id):
    """
    Возвращает настройки сервера "реакции-роли"

    :param guild_id: id сервера
    :return: настройки сервера "реакции-роли"
    """
    return CategoryRole().get(guild_id)


def check_msg_delete(msg_id: int, guild_id: int):
    db = ReactionRole()
    if msg_id == db.get_msg_id(guild_id):
        db.delete("id", msg_id)
