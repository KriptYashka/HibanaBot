import discord
from discord.ext import commands
from models.db.reaction_msg import MessageReaction, SettingRole


async def give_roles(bot: commands.Bot, msg: discord.Message):
    setting_roles = SettingRole().get(msg.guild.id)
    if not setting_roles:
        return await msg.channel.send(f'Не настроены роли для сервера\nid: `{msg.guild.id}`')

    old_msg_id = MessageReaction().get_msg_id(msg.guild.id)
    if old_msg_id:
        return await msg.channel.send(f"Уже существует сообщение с ролями:\n"
                                      f"https://discord.com/channels/{msg.guild.id}/{msg.channel.id}/{old_msg_id}")
    new_msg = await msg.channel.send('Give roles!')
    if new_msg:
        MessageReaction().add(new_msg)
        for emoji in setting_roles:
            await new_msg.add_reaction(emoji)


def is_role_message(message_id: int) -> bool:
    return MessageReaction().is_exist_msg(message_id)


def get_setting_roles(guild_id):
    return SettingRole().get(guild_id)


def check_msg_delete(msg_id: int, guild_id: int):
    db = MessageReaction()
    if msg_id == db.get_msg_id(guild_id):
        db.delete("id", msg_id)
