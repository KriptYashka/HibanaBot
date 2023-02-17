import discord
from discord import app_commands as ac


@ac.command()
async def add(interaction: discord.Interaction, first_value: int = 0, second_value: int = 0):
    """Adds two numbers together.

    :param first_value: Число 1
    :param second_value: Число 2
    """
    await interaction.response.send_message(f'Проверка')
