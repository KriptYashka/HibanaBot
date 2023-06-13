from typing import List

import discord
from discord import app_commands as ac

from handlers.get_select_roles import ReactionRoleHandler, CategoryHandler


@ac.command(name="reaction_add")
async def add(interaction: discord.Interaction, role: discord.Role, emoji: str):
    """
    Добавляет реакцию на соответствующую роль

    :param interaction: Объект интерактива
    :param role: Роль на сервере
    :param emoji: Эмодзи для выбора роли
    """
    try:
        ReactionRoleHandler().add(guild_id=interaction.guild_id, role_id=role.id, emoji=emoji)
    except Exception as e:
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.'
    else:
        text = f'Роль {role.mention} ({emoji}) успешно добавлена в систему ролей вашего сервера.'

    await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="reaction_set")
async def set_reaction(interaction: discord.Interaction, role: str, category: str):
    """
    Добавляет роль-реакцию в категорию

    :param interaction: Объект интерактива
    :param role: Роль на сервере
    :param category: Название категории, к которой крепится реакция
    """
    try:
        category_id = CategoryHandler().get(interaction.guild_id, category)[0][0]
        role = interaction.guild.get_role(int(role))
        ReactionRoleHandler().edit(f"guild_id='{interaction.guild_id}' AND role_id='{role.id}'",
                                   category_id=category_id)
    except Exception as e:
        print(e)
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.'
    else:
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
    try:
        category_id = CategoryHandler().get(interaction.guild_id, category)[0][0]
        role = interaction.guild.get_role(int(role))
        where_expr = f"guild_id='{interaction.guild_id}' AND role_id='{role.id}' AND category_id={category_id}"
        ReactionRoleHandler().edit(where_expr, category_id=None)
        # TODO: Проверка, есть ли данная реакция в категории
    except Exception as e:
        print(e)
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.'
    else:
        text = f'Роль {role.mention} убрана с категории **{category}**!'

    await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="reaction_delete")
async def delete(interaction: discord.Interaction, role: discord.Role):
    """
    Удаляет реакцию с соответствующей роли

    :param interaction: Объект интерактива
    :param role: Роль на сервере
    """
    try:
        ReactionRoleHandler().delete(guild_id=interaction.guild_id, role_id=role)
    except Exception as e:
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.'
    else:
        text = f'Роль {role.mention} исключена из системы получения ролей.'

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
