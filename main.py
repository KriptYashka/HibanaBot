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
        item.guild_only = True
        bot.tree.add_command(item)

    bot.run(token=token)


@bot.event
async def on_ready():
    await bot.tree.sync()


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    print("Это типо сработало")
    await ctx.interaction.response.send_message(content="У вас недостаточно прав для совершения данного действия",
                                                ephemeral=True, delete_after=2)


@bot.event
async def on_raw_message_delete(payload: discord.RawMessageDeleteEvent):
    handler = CategoryMessageHandler()
    if CategoryMessageHandler().is_exist_msg(payload.message_id, payload.guild_id):
        handler.delete(msg_id=payload.message_id, channel_id=payload.channel_id, guild_id=payload.guild_id)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if bot.get_user(payload.user_id).bot:
        return
    if category_msg := CategoryMessageHandler().get(payload.guild_id, payload.channel_id, payload.message_id):
        data = [f"guild_id={payload.guild_id}", f"emoji='{payload.emoji}'", f"category='{category_msg[3]}'"]
        where_expr = " AND ".join(data)
        if react_roles := ReactionRoleHandler().select(where_expr):
            data = react_roles[0]
            guild = bot.get_guild(payload.guild_id)
            r = guild.get_role(data[2])
            await payload.member.add_roles(r)
            # await payload.member.send(f"Роль `{r}` добавлена на сервере `{guild}`")


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if bot.get_user(payload.user_id).bot:
        return
    if category_msg := CategoryMessageHandler().get(payload.guild_id, payload.channel_id, payload.message_id):
        data = [f"guild_id={payload.guild_id}", f"emoji='{payload.emoji}'", f"category='{category_msg[3]}'"]
        where_expr = " AND ".join(data)
        if react_roles := ReactionRoleHandler().select(where_expr):
            data = react_roles[0]
            guild = bot.get_guild(payload.guild_id)
            r = guild.get_role(data[2])
            member = guild.get_member(payload.user_id)
            await member.remove_roles(r)
            # await member.send(f"Роль `{r}` убрана на сервере `{guild}`")


if __name__ == '__main__':
    main()
