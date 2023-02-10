import os

import discord
from discord.ext import commands

from discord_token import token
from views import main_view, r6_view
from settings import Settings

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=Settings.PREFIX, intents=intents)


@bot.event
async def on_message(msg: discord.Message):
    if msg.author.bot:
        return
    msg.content = msg.content.strip(Settings.PREFIX)
    if msg.content.startswith("roles"):
        new_msg = await msg.channel.send('Give roles!')
        list_emoji = ["😄", "🦆", "🐱",]
        for emoji in list_emoji:
            await new_msg.add_reaction(emoji)
    new_msg = await msg.channel.send('pong')


bot.run(token=token)
