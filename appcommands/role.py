import discord
from discord import app_commands as ac

from handlers import role as h_role


@ac.command(name="reaction_add")
async def add_reaction(interaction: discord.Interaction, role: discord.Role, emoji: str):
    """
    Добавляет реакцию на соответствующую роль

    :param interaction: Объект интерактива
    :param role: Роль на сервере
    :param emoji: Эмодзи для выбора роли
    """
    try:
        await h_role.add_reaction_role(interaction.guild_id, role, emoji)
    except Exception as e:
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.',
    else:
        text = f'Роль {role.mention} ({emoji}) успешно добавлена в систему ролей вашего сервера.',

    await interaction.response.send_message(content=text, ephemeral=True)