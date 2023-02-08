import discord
from discord.ext import commands

from cmd import main_view, r6_view

bot = commands.Bot(command_prefix='!')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run('token')
