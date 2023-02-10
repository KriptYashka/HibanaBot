import discord
from discord.ext import commands
from models.db.reaction_msg import MessageReaction, SettingRole


def save_msg_reaction(msg: discord.Message):
    db = MessageReaction()
    db.add(msg)


def guild_setting_roles(guild_id: int) -> dict[str, int]:
    db = SettingRole()
    return db.get(guild_id)
