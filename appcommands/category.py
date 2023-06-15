from typing import List

import discord
from discord import app_commands as ac

from get_select_roles import CategoryHandler, ReactionRoleHandler
from appcommands.role import set_reaction
from settings import Settings


@ac.command(name="category_add")
async def add(interaction: discord.Interaction,
              title: str,
              description: str = None,
              mutually_exclusive: bool = True,
              ):
    """
    Добавляет категорию для реакций

    :param interaction: Объект интерактива
    :param title: Название категории
    :param description: Описание категории, которое будет отображаться пользователям
    :param mutually_exclusive: Можно ли получить только 1 роль в категории
    """
    handler = CategoryHandler()
    category_count = handler.count_guild_categories(interaction.guild_id)
    if category_count >= Settings.LIMIT_CATEGORY_COUNT:
        text = f'На сервере превышен лимит категорий.\nМаксимум {Settings.LIMIT_CATEGORY_COUNT} категорий.'
        return await interaction.response.send_message(content=text, ephemeral=True)

    handler.add(guild_id=interaction.guild_id, title=title,
                description=description, mutually_exclusive=mutually_exclusive)
    text = f'Категория **{title}** успешно добавлена в систему ролей вашего сервера.'
    return await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="category_show")
async def show(interaction: discord.Interaction, title: str = None):
    """
    Отображает все Embed категорий на сервере

    :param interaction: Объект интерактива
    :param title: Название категории
    """
    handler = CategoryHandler()
    categories = handler.get(interaction.guild_id, title)
    if not len(categories):
        text = "На данном сервере нет категорий ролей"
        return await interaction.response.send_message(content=text, ephemeral=True)
    embeds = [handler.get_embed_show(data, interaction.guild) for data in categories]
    await interaction.response.send_message(embeds=embeds, ephemeral=True)


@ac.command(name="category_create")
async def create(interaction: discord.Interaction, title: str = None):
    """
    Выводит в чат Embed категории с реакциями

    :param interaction: Объект интерактива
    :param title: Название категории
    """
    h_category = CategoryHandler()
    h_role = ReactionRoleHandler()
    category = h_category.get(interaction.guild_id, title)
    if not len(category):
        text = "На данном сервере нет категорий ролей"
        return await interaction.response.send_message(content=text, ephemeral=True)
    reactions = h_role.get_by_category(interaction.guild_id, category[1])
    emojis = [item[4] for item in reactions] if reactions else []
    embed = h_category.get_embed_for_create(category, interaction.guild)
    await interaction.response.send_message(embed=embed)
    inter_msg = await interaction.original_response()
    for react in emojis:
        await inter_msg.add_reaction(react)


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
    h_category = CategoryHandler()
    try:
        h_category.edit(f"title=\"{title}\" AND guild_id={interaction.guild_id}",
                        title=new_title,
                        description=new_description,
                        mutually_exclusive=mutually_exclusive)
    except Exception as e:
        print(e)
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.'
        await interaction.response.send_message(content=text, ephemeral=True)
    else:
        current_title = new_title if new_title else title
        new_category_data = h_category.get(interaction.guild_id, current_title)
        embed = h_category.get_embed_show(new_category_data, interaction.guild)
        await interaction.response.send_message(embed=embed, ephemeral=True)


@ac.command(name="category_delete")
async def delete(interaction: discord.Interaction, title: str):
    """
    Удаляет категорию с выбранного сервера

    :params title: Название категории на сервере
    """
    text = f"Операция успешно провалена. Категории '**{title}**' не существует на данном сервере."
    if is_deleted := CategoryHandler().delete(guild_id=interaction.guild_id, title=title):
        where_expr = f"guild_id={interaction.guild_id} AND category='{title}'"
        ReactionRoleHandler().edit(where_expr, category="NULL")
        text = "Операция успешно завершена. Категория удалена."
    await interaction.response.send_message(content=text, ephemeral=True)


@edit.autocomplete('title')
@show.autocomplete('title')
@create.autocomplete('title')
@delete.autocomplete('title')
@set_reaction.autocomplete('category')
async def category_autocomplete(interaction: discord.Interaction, current: str) -> List[ac.Choice[str]]:
    categories = CategoryHandler().get(interaction.guild_id)
    if not categories:
        return []
    categories_name = [category[1] for category in categories]
    return [
        ac.Choice(name=name, value=name) for name in categories_name if current.lower() in name.lower()
    ]
