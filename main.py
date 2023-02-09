import discord
from discord.ext import commands

from views import main_view, r6_view

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run('token')
