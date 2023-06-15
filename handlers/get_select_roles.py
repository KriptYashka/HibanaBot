from typing import Optional, Union

import discord

from base import BaseHandler
from db import category, role


class CategoryHandler(BaseHandler):
    """
    Используйте данный обработчик для работы с категориями и сообщениями категорий на сервере.
    """

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
        return response_category[0] if title else response_category or None

    @staticmethod
    def get_embed_show(data: list, guild: discord.Guild) -> Optional[discord.Embed]:
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
        text = CategoryHandler.get_text_role_category(data, guild)
        embed.add_field(name="Доступны следующие роли", value=text)
        answer = "Да" if data[3] else "Нет"
        embed.add_field(name=f"Можно участникам с ролями данной категории получить новую роль:",
                        value=answer, inline=False)
        return embed

    @staticmethod
    def get_embed_for_create(data: list, guild: discord.Guild) -> Optional[discord.Embed]:
        if len(data) < 4:
            return None
        embed = discord.Embed()
        embed.title = f"__{data[1]}__"
        embed.colour = 0x7d17bb
        if data[2]:
            embed.add_field(name=f"Описание", value=data[2], inline=False)
        text = CategoryHandler.get_text_role_category(data, guild)
        embed.add_field(name="Доступны следующие роли", value=text)
        if not data[3]:
            embed.set_footer(text="Можно получить только одну роль")
        return embed

    @staticmethod
    def get_text_role_category(data, guild):
        if react_roles := ReactionRoleHandler().get_by_category(guild_id=data[0], category_title=data[1]):
            text = ""
            for react in react_roles:
                role_id, emoji = react[2], react[4]
                role_ins = guild.get_role(role_id)
                text += f"Роль {role_ins.mention}  - {emoji}\n"
        else:
            text = "У данной категории нет ролей. Она. Просто. Существует."
        return text

    def count_guilds(self) -> int:
        """
        Возвращает количество серверов, на которых используются категории.
        """
        return self.db.get_count_rows("DISTINCT guild_id")

    def count_guild_categories(self, guild_id: int) -> int:
        """
        Возвращает количество созданных категорий на сервере (не сообщений).
        """
        return self.db.get_count_rows(where_expr=f"guild_id={guild_id}")


class CategoryMessageHandler(BaseHandler):
    """
    Используйте данный обработчик для работы с сообщениями категорий на сервере.
    """

    def __init__(self):
        super().__init__(category.CategoryMessage())

    def get_guild_category_msg(self, guild_id: int, title: str) -> Optional[list]:
        """
        Возвращает сообщение категории на сервере, если есть.
        """
        res = self.db.select(where_expr=f"guild_id={guild_id} AND category='{title}'")
        return res[0] if res else None

    def is_exist_msg(self, msg_id: int, guild_id: int) -> bool:
        return bool(self.db.select(where_expr=f"guild_id={guild_id} AND msg_id={msg_id}")[0])


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

    def get(self, guild_id: int, role_id: int = None, category_title: str = None) -> Optional[list]:
        """
        Возвращает роли сервера
        """
        where_expr = f"guild_id={guild_id}"
        if role_id:
            where_expr += f" AND role_id={role_id}"
        res = self.db.select(where_expr)
        return res or None

    def get_by_category(self, guild_id: int, category_title: str) -> Optional[list]:
        """
        Возвращает роли категории на сервере
        """
        where_expr = f"guild_id={guild_id} AND category='{category_title}'"
        res = self.db.select(where_expr)
        return res or None
