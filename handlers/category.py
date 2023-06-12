from typing import List, Optional

import discord

from models import entity
from models.db.category import CategoryRole


def add(**kwargs):
    """
    Обработчик создания новой категории ролей
    """
    CategoryRole().insert(kwargs)


def edit(guild_id: int, old_title: str, **kwargs):
    """
    Обработчик изменения категории ролей
    """
    CategoryRole().update(kwargs, where_expr=f"title='{old_title}' AND guild_id={guild_id}")


def get_data(guild_id: int, title: str = None) -> List:
    where_expr = f"guild_id={guild_id}"
    if title:
        where_expr += f" AND title='{title}'"
    response_category = CategoryRole().select(where_expr=where_expr)
    return response_category


def get_embed(category: tuple) -> Optional[discord.Embed]:
    """
    Создает Embed для категории

    :category: Кортеж с данными категории
    """
    if len(category) < 4:
        return None
    embed = discord.Embed()
    embed.title = f"Категория __{category[1]}__"
    embed.colour = 0x7d17bb
    answer = category[2] if category[2] else "Нет"
    embed.add_field(name=f"Описание", value=answer, inline=False)
    answer = "Да" if category[3] else "Нет"
    embed.add_field(name=f"Можно участникам с ролями данной категории получить новую роль:",
                    value=answer, inline=False)
    return embed


def delete(guild_id: int, title: str) -> bool:
    db = CategoryRole()
    data = {
        "title": title,
        "guild_id": guild_id,
    }
    if is_exist := db.select(where_expr=" AND ".join([f"{key} = '{value}'" for key, value in data.items()])):
        CategoryRole().delete(data)
    return is_exist

