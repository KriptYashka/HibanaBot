import discord
from discord import app_commands as ac

from handlers import roles


@ac.command()
async def add_reaction(interaction: discord.Interaction, role: discord.Role, emoji: str):
    """
    Добавляет реакцию на соответствующую роль

    :param interaction: Объект интерактива
    :param role: Роль на сервере
    :param emoji: Эмодзи для выбора роли
    """
    try:
        await roles.add_reaction_role(interaction, role, emoji)
    except Exception as e:
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.',
    else:
        text = f'Роль {role.mention} ({emoji}) успешно добавлена в систему ролей вашего сервера.',

    await interaction.response.send_message(content=text, ephemeral=True)


@ac.command()
async def add_category(interaction: discord.Interaction, title: str, description: str = None):
    """
    Добавляет категорию для реакций

    :param interaction: Объект интерактива
    :param title: Название категории
    :param description: Описание категории, которое будет отображаться пользователям
    """
    try:
        await roles.add_category(interaction, title, description)
    except Exception as e:
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.'
    else:
        text = f'Категория {title} успешно добавлена в систему ролей вашего сервера.'

    await interaction.response.send_message(content=text, ephemeral=True)
