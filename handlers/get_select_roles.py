from typing import Optional, Union

import discord

from base import BaseHandler
from db import category, role


class CategoryHandler(BaseHandler):
    def __init__(self):
        super().__init__(category.CategoryRole())

    def get(self, guild_id: int, title: str = None) -> Optional[list]:
        """
        Возвращает записи из БД с категориями сервера. \n
        -- При указании *title* возвращается одномерный список категории. \n
        -- При отсутствии результатов, возвращается *None*

        :return: Двумерный (без title) или одномерный (с title) список записей категорий сервера.
        """
        where_expr = f"guild_id={guild_id}"
        if title:
            where_expr += f" AND title='{title}'"
        response_category = self.db.select(where_expr=where_expr)
        return response_category[0] if title else response_category if response_category else None

    @staticmethod
    def get_embed(data: tuple) -> Optional[discord.Embed]:
        """
        Создает Embed для категории

        :category: Кортеж с данными из БД категории
        """
        if len(data) < 4:
            return None
        embed = discord.Embed()
        embed.title = f"Категория __{data[1]}__"
        embed.colour = 0x7d17bb
        answer = data[2] if data[2] else "Нет"
        embed.add_field(name=f"Описание", value=answer, inline=False)
        answer = "Да" if data[3] else "Нет"
        embed.add_field(name=f"Можно участникам с ролями данной категории получить новую роль:",
                        value=answer, inline=False)
        return embed


class ReactionRoleHandler(BaseHandler):
    def __init__(self):
        super().__init__(role.ReactionRole())

    def is_role_message(self, message_id: int) -> bool:  # TODO: Переназвать
        """
        Является ли сообщение вида "реакция-роль".

        :param message_id: id сообщения
        :return: True или False
        """
        return bool(self.db.select(f"id={message_id}"))

    def get(self, guild_id: int, role_id: int = None, category_id: int = None) -> Optional[list]:
        """
        Возвращает роли сервера из БД
        """
        where_expr = f"guild_id={guild_id}"
        if role_id:
            where_expr += f" AND role_id={role_id}"
        res = self.db.select(where_expr)
        return res if res != [] else None
