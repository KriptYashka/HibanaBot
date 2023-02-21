from typing import List
from models.db.category import CategoryRole


def add(**kwargs):
    """
    Обработчик создания новой категории ролей
    """
    CategoryRole().insert(kwargs)


def edit(guild_id: int, current_title: str, **kwargs):
    """
    Обработчик изменения категории ролей
    """
    return CategoryRole().update(kwargs, where_expr=f"title='{current_title}' AND guild_id={guild_id}")


def get_by_guild(guild_id: int, current_title: str = None):
    if current_title is None:
        where_expr = f"guild_id={guild_id}"
        return CategoryRole().select(where_expr=where_expr)
    else:
        where_expr = f"title='{current_title}' AND guild_id={guild_id}"
        return None if not (category := CategoryRole().select(where_expr=where_expr)) else category[0]
