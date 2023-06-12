from typing import List

import discord
from discord import app_commands as ac

import handlers.category
from handlers.category import get_embed


@ac.command(name="category_add")
async def add(interaction: discord.Interaction,
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


@ac.command(name="category_show")
async def show(interaction: discord.Interaction, title: str = None):
    """
    Добавляет категорию для реакций

    :param mutually_exclusive:
    :param interaction: Объект интерактива
    :param title: Название категории
    :param description: Описание категории, которое будет отображаться пользователям
    """
    categories = handlers.category.get_data(guild_id=interaction.guild_id, title=title)
    if not len(categories):
        text = "На данном сервере нет категорий ролей"
        return await interaction.response.send_message(content=text, ephemeral=True)
    embeds = list()
    for category in categories:
        embed = get_embed(category)
        embeds.append(embed)
    await interaction.response.send_message(embeds=embeds, ephemeral=True)


@ac.command(name="category_edit")
async def edit(interaction: discord.Interaction,
               title: str,
               new_title: str = None,
               new_description: str = None,
               mutually_exclusive: bool = None,
               ):
    """
    Добавляет категорию для реакций

    :param mutually_exclusive: Разрешение на получение нескольких ролей в данной категории.
    :param new_title: Новый заголовок категории
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
        new_category = handlers.category.get_data(interaction.guild_id, current_title)[0]
        embed = get_embed(new_category)
        await interaction.response.send_message(embed=embed, ephemeral=True)


@ac.command(name="category_delete")
async def delete(interaction: discord.Interaction, title: str):
    """
    Удаляет категорию с выбранного сервера

    :params title: Название категории на сервере
    """
    guild_id = interaction.guild_id
    is_deleted = handlers.category.delete(guild_id, title)
    if is_deleted:
        text = "Операция успешно завершена. Категория удалена."
    else:
        text = f"Операция успешно провалена. Категории '**{title}**' не существует на данном сервере."
    await interaction.response.send_message(content=text, ephemeral=True)


@edit.autocomplete('title')
@show.autocomplete('title')
@delete.autocomplete('title')
async def category_autocomplete(interaction: discord.Interaction, current: str) -> List[ac.Choice[str]]:
    categories = handlers.category.get_data(interaction.guild_id)
    categories_name = [category[1] for category in categories]
    return [
        ac.Choice(name=name, value=name) for name in categories_name if current.lower() in name.lower()
    ]
