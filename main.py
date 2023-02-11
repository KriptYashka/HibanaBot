import os

import discord
from discord.ext import commands

from discord_token import token
from views import main_view, r6_view
from models.create_tables import init_tables
from settings import Settings

init_tables()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=Settings.PREFIX, intents=intents)

actions = {
    "roles": main_view.msg_roles,
}


@bot.event
async def on_message(msg: discord.Message):
    if msg.author.bot:
        return
    for cmd, action in actions.items():
        if msg.content.startswith(cmd):
            await action(bot, msg)


@bot.event
async def on_raw_message_delete(payload: discord.RawMessageDeleteEvent):
    main_view.check_msg_delete(payload.message_id, payload.guild_id)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if bot.get_user(payload.user_id).bot:
        return
    if main_view.is_role_message(payload.message_id):
        guild = bot.get_guild(payload.guild_id)
        setting_roles = main_view.get_setting_roles(payload.guild_id)
        role = discord.utils.get(guild.roles, id=setting_roles[payload.emoji.name])  # TODO: Обработку ошибки
        await payload.member.add_roles(role)
        await payload.member.send(f"`{role}` роль добавлена на сервере `{guild}`")


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if bot.get_user(payload.user_id).bot:
        return
    if main_view.is_role_message(payload.message_id):
        guild = bot.get_guild(payload.guild_id)
        setting_roles = main_view.get_setting_roles(payload.guild_id)
        role = discord.utils.get(guild.roles, id=setting_roles[payload.emoji.name])  # TODO: Обработку ошибки
        member = guild.get_member(payload.user_id)
        await member.remove_roles(role)
        await member.send(f"`{role}` роль убрана на сервере `{guild}`")


bot.run(token=token)
