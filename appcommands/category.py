from typing import List

import discord
from discord import app_commands as ac

import handlers.category
from handlers import role as role_h


@ac.command(name="category_add")
async def add_category(interaction: discord.Interaction,
                       title: str,
                       description: str = None,
                       mutually_exclusive: bool = True,
                       ):
    """
    Добавляет категорию для реакций

    :param mutually_exclusive:
    :param interaction: Объект интерактива
    :param title: Название категории
    :param description: Описание категории, которое будет отображаться пользователям
    """
    try:
        handlers.category.add(guild_id=interaction.guild_id,
                              title=title,
                              description=description,
                              mutually_exclusive=mutually_exclusive,
                              )
    except Exception as e:
        print(e)
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.'
    else:
        text = f'Категория **{title}** успешно добавлена в систему ролей вашего сервера.'

    await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="category_edit")
async def edit_category(interaction: discord.Interaction,
                        title: str,
                        new_title: str = None,
                        new_description: str = None,
                        mutually_exclusive: bool = None,
                        ):
    """
    Добавляет категорию для реакций

    :param mutually_exclusive:
    :param new_title:
    :param interaction: Объект интерактива
    :param title: Название категории
    :param new_description: Описание категории, которое будет отображаться пользователям
    """
    try:
        handlers.category.edit(interaction.guild_id,
                               title,
                               title=new_title,
                               description=new_description,
                               mutually_exclusive=mutually_exclusive
                               )
    except Exception as e:
        print(e)
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.'
        await interaction.response.send_message(text=text, ephemeral=True)
    else:
        current_title = new_title if new_title else title
        new_category = handlers.category.get_by_guild(interaction.guild_id, current_title)
        title = new_category[1]
        desc = new_category[2]
        mutex = new_category[3]

        embed = discord.Embed()
        embed.title=f"Категория - {title}"
        embed.colour=0x7d17bb
        embed.add_field(name="Описание:", value=desc, inline=True)
        embed.add_field(name="Можно участникам с ролями данной категории получить новую роль:", value=mutex, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)


@edit_category.autocomplete('title')
async def category_autocomplete(interaction: discord.Interaction, current: str) -> List[ac.Choice[str]]:
    categories = handlers.category.get_by_guild(interaction.guild_id)
    categories_name = [category[1] for category in categories]
    return [
        ac.Choice(name=name, value=name) for name in categories_name if current.lower() in name.lower()
    ]
