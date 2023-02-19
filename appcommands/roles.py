from typing import List, Optional

import discord
from discord import app_commands as ac

from handlers import roles


@ac.command(name="reaction_add")
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


@ac.command(name="category_add")
async def add_category(interaction: discord.Interaction, title: str, description: str = None):
    """
    Добавляет категорию для реакций

    :param interaction: Объект интерактива
    :param title: Название категории
    :param description: Описание категории, которое будет отображаться пользователям
    """
    try:
        await roles.add_category(interaction.guild_id, title, description)
    except Exception as e:
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.'
    else:
        text = f'Категория **{title}** успешно добавлена в систему ролей вашего сервера.'

    await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="category_edit")
async def edit_category(interaction: discord.Interaction, category: str, new_title: str = None,
                        new_description: str = None, mutually_exclusive: bool = None):
    """
    Добавляет категорию для реакций

    :param interaction: Объект интерактива
    :param category: Название категории
    :param new_description: Описание категории, которое будет отображаться пользователям
    """
    try:
        data = {

        }
        await roles.edit_category(interaction.guild_id,
                                  category,
                                  title=new_title,
                                  description=new_description,
                                  mutually_exclusive=mutually_exclusive
                                  )
    except Exception as e:
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.'
    else:
        text = f'Категория **{category}** успешно изменена.'

    await interaction.response.send_message(content=text, ephemeral=True)


@edit_category.autocomplete('category')
async def category_autocomplete(interaction: discord.Interaction, current: str) -> List[ac.Choice[str]]:
    categories = roles.get_category_roles(interaction.guild_id)
    categories_name = [category[1] for category in categories]
    return [
        ac.Choice(name=name, value=name) for name in categories_name if current.lower() in name.lower()
    ]


@edit_category.autocomplete('mutually_exclusive')
async def category_autocomplete(interaction: discord.Interaction, current: str) -> List[ac.Choice[str]]:
    categories_name = [False, True]
    return [
        ac.Choice(name="name", value=name) for name in categories_name
    ]
