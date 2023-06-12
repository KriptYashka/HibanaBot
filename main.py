import os

import discord
from discord.ext import commands

import appcommands.category
import handlers.category
from discord_token import token
from handlers import role as h_role
from models.create_tables import init_tables
from settings import Settings

from appcommands import role

init_tables()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=Settings.PREFIX, intents=intents)
bot.tree.copy_global_to(guild=discord.Object(id=757331809108230254))

bot.tree.add_command(role.add_reaction)
bot.tree.add_command(appcommands.category.add)
bot.tree.add_command(appcommands.category.edit)
bot.tree.add_command(appcommands.category.show)
bot.tree.add_command(appcommands.category.delete)


@bot.event
async def on_ready():
    await bot.tree.sync()


@bot.event
async def on_raw_message_delete(payload: discord.RawMessageDeleteEvent):
    h_role.check_msg_delete(payload.message_id, payload.guild_id)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if bot.get_user(payload.user_id).bot:
        return
    if h_role.is_role_message(payload.message_id):
        guild = bot.get_guild(payload.guild_id)
        setting_roles = handlers.category.get_guild_categories(payload.guild_id)
        role = discord.utils.get(guild.roles, id=setting_roles[payload.emoji.name])  # TODO: Обработку ошибки
        await payload.member.add_roles(role)
        await payload.member.send(f"`{role}` роль добавлена на сервере `{guild}`")


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if bot.get_user(payload.user_id).bot:
        return
    if h_role.is_role_message(payload.message_id):
        guild = bot.get_guild(payload.guild_id)
        setting_roles = handlers.category.get_guild_categories(payload.guild_id)
        role = discord.utils.get(guild.roles, id=setting_roles[payload.emoji.name])  # TODO: Обработку ошибки
        member = guild.get_member(payload.user_id)
        await member.remove_roles(role)
        await member.send(f"`{role}` роль убрана на сервере `{guild}`")


bot.run(token=token)
