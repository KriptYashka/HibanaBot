from typing import List
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
    return CategoryRole().update(kwargs, where_expr=f"title='{old_title}' AND guild_id={guild_id}")


def get(guild_id: int, title: str = None) -> List:
    where_expr = f"guild_id={guild_id}"
    if title:
        where_expr = f"title='{title}' AND guild_id={guild_id}"
    return CategoryRole().select(where_expr=where_expr)
