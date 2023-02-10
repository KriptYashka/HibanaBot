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


@bot.event
async def on_message(msg: discord.Message):
    if msg.author.bot:
        return
    if msg.content.startswith("roles"):
        setting_roles = main_view.guild_setting_roles(msg.guild.id)
        if not setting_roles:
            return await msg.channel.send(f'Не настроены роли для сервера\nid: `{msg.guild.id}`')

        new_msg = await msg.channel.send('Give roles!')
        main_view.save_msg_reaction(new_msg)
        for emoji in setting_roles:
            await new_msg.add_reaction(emoji)



bot.run(token=token)
