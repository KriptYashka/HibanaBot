from typing import List, Optional

import discord
from discord import app_commands as ac
import emoji

from handlers.get_select_roles import ReactionRoleHandler, CategoryHandler


@ac.command(name="reaction_add")
async def add(interaction: discord.Interaction, role: discord.Role, emoji_str: str):
    """
    Добавляет реакцию на соответствующую роль

    :param interaction: Объект интерактива
    :param role: Роль на сервере
    :param emoji_str: Эмодзи для выбора роли
    """
    db_role = ReactionRoleHandler().get(guild_id=interaction.guild_id, role_id=role.id)

    # Проверка на валидность
    if db_role:
        text = f'Роль {role.mention} ({db_role[0][4]}) уже существует. Выберите другую роль.'
        return await interaction.response.send_message(content=text, ephemeral=True)
    emojis_str = [str(item) for item in interaction.guild.emojis]
    if not (emoji.is_emoji(emoji_str) or emoji_str in emojis_str):
        text = f'Реакция ({emoji_str}) не является стандартным эмоджи. Выберите другую реакцию.'
        return await interaction.response.send_message(content=text, ephemeral=True)

    ReactionRoleHandler().add(guild_id=interaction.guild_id, role_id=role.id, emoji=emoji_str)
    text = f'Роль {role.mention} ({emoji_str}) успешно добавлена в систему ролей вашего сервера.'
    await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="reaction_show")
async def show(interaction: discord.Interaction, only_free: bool = False):
    """
    Показывает все роли с реакциями и в каких категориях их можно получить

    :param interaction: Объект интерактива
    :param only_free: Отображение только свободных ролей
    """
    h_category = CategoryHandler()
    h_role = ReactionRoleHandler()

    roles = h_role.select(f"guild_id={interaction.guild_id} AND category_id is NULL")
    text = ""
    embeds = []
    if roles:
        for role_data in roles:
            role = interaction.guild.get_role(role_data[2])
            text += f"{role.mention} --> {role_data[4]}\n"
        embed = discord.Embed(colour=0xff0000, title="Роли без категорий", description=text)
        embeds.append(embed)

    if only_free:
        if embeds:
            return await interaction.response.send_message(embeds=embeds, ephemeral=True)
        return await interaction.response.send_message(content="Нет нераспределенных ролей.", ephemeral=True)

    categories_db = h_category.get(interaction.guild_id)
    for category in categories_db:
        embed = h_category.get_embed(category)
        roles = h_role.select(f"guild_id={interaction.guild_id} AND category_id={category[0]}")
        text = ""
        for role_data in roles:
            role = interaction.guild.get_role(role_data[2])
            text += f"{role.mention} --> {role_data[4]}\n"
        embed.add_field(name="Можно получть следующие роли", value=text)
        embeds.append(embed)

    if embeds:
        return await interaction.response.send_message(embeds=embeds, ephemeral=True)
    text = f"Нет ролей. Используйте команду /{add.name} для добавления роли."
    return await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="reaction_set")
async def set_reaction(interaction: discord.Interaction, role: str, category: str):
    """
    Добавляет роль-реакцию в категорию

    :param interaction: Объект интерактива
    :param role: Название роли на сервере
    :param category: Название категории, к которой крепится реакция
    """
    if not (category_data := CategoryHandler().get(interaction.guild_id, category)):
        text = f"Категории {category} не существует на данном сервере."
        return await interaction.response.send_message(content=text, ephemeral=True)
    role = interaction.guild.get_role(int(role))
    ReactionRoleHandler().edit(f"guild_id='{interaction.guild_id}' AND role_id='{role.id}'",
                               category_id=category_data[0])
    text = f'Роль {role.mention} добавлена к категории **{category}**!'
    await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="reaction_unset")
async def unset_reaction(interaction: discord.Interaction, category: str, role: str):
    """
    Убирает роль-реакцию с категории

    :param interaction: Объект интерактива
    :param role: Роль на сервере
    :param category: Название категории, от которой открепляется реакция
    """
    if not (category_data := CategoryHandler().get(interaction.guild_id, category)):
        text = f"Категории {category} не существует на данном сервере."
        return await interaction.response.send_message(content=text, ephemeral=True)
    role = interaction.guild.get_role(int(role))
    where_expr = f"guild_id='{interaction.guild_id}' AND role_id='{role.id}' AND category_id={category_data[0]}"
    ReactionRoleHandler().edit(where_expr, category_id=None)

    text = f'Роль {role.mention} убрана с категории **{category}**!'
    await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="reaction_delete")
async def delete(interaction: discord.Interaction, role: discord.Role):
    """
    Удаляет реакцию с соответствующей роли

    :param interaction: Объект интерактива
    :param role: Роль на сервере
    """
    is_exist = ReactionRoleHandler().delete(guild_id=interaction.guild_id, role_id=role)
    text = f'Роль {role.mention} исключена из системы получения ролей.'
    if is_exist:
        text = f"Роль {role.mention} не привязана. В текущий момент она не была добавлена в систему получения ролей."
    await interaction.response.send_message(content=text, ephemeral=True)


@set_reaction.autocomplete('role')
@unset_reaction.autocomplete('role')
async def set_reaction_autocomplete(interaction: discord.Interaction, current: str) -> List[ac.Choice[str]]:
    db_roles = ReactionRoleHandler().get(interaction.guild_id)
    db_role_ids = [role[2] for role in db_roles]
    role_names = [(role.name, str(role.id)) for role in interaction.guild.roles if role.id in db_role_ids]
    return [
        ac.Choice(name=name, value=i) for name, i in role_names if current.lower() in name.lower()
    ]
