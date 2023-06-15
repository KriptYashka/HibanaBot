import os
from typing import Optional

import discord
from discord.ext import commands
from discord_token import token

from appcommands import category, role
from handlers.get_select_roles import CategoryHandler, CategoryMessageHandler, ReactionRoleHandler
from models.create_tables import init_tables
from settings import Settings

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=Settings.PREFIX, intents=intents)


def main():
    global bot
    init_tables()

    bot.tree.copy_global_to(guild=discord.Object(id=757331809108230254))

    cmd = [role.add, role.show, role.set_reaction, role.unset_reaction, role.delete,
           category.add, category.edit, category.show, category.create, category.delete]

    for item in cmd:
        bot.tree.add_command(item)

    bot.run(token=token)


@bot.event
async def on_ready():
    await bot.tree.sync()


@bot.event
async def on_raw_message_delete(payload: discord.RawMessageDeleteEvent):
    handler = CategoryMessageHandler()
    if CategoryMessageHandler().is_exist_msg(payload.message_id, payload.guild_id):
        handler.delete(msg_id=payload.message_id, channel_id=payload.channel_id, guild_id=payload.guild_id)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if bot.get_user(payload.user_id).bot:
        return
    if CategoryMessageHandler().is_exist_msg(payload.message_id, payload.guild_id):
        guild = bot.get_guild(payload.guild_id)
        # ReactionRoleHandler().get_by_category()
        # role = discord.utils.get(guild.roles, id=setting_roles[payload.emoji.name])
        # await payload.member.add_roles(role)
        # await payload.member.send(f"`{role}` роль добавлена на сервере `{guild}`")


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if bot.get_user(payload.user_id).bot:
        return
    # if h_role.is_role_message(payload.message_id):
    #     guild = bot.get_guild(payload.guild_id)
    #     setting_roles = handlers.category.get_guild_categories(payload.guild_id)
    #     role = discord.utils.get(guild.roles, id=setting_roles[payload.emoji.name])  # TODO: Обработку ошибки
    #     member = guild.get_member(payload.user_id)
    #     await member.remove_roles(role)
    #     await member.send(f"`{role}` роль убрана на сервере `{guild}`")


if __name__ == '__main__':
    main()
