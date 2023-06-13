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
        await ReactionRoleHandler().add(guild_id=interaction.guild_id, role_id=role.id, emoji=emoji)
    except Exception as e:
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.'
    else:
        text = f'Роль {role.mention} ({emoji}) успешно добавлена в систему ролей вашего сервера.'

    await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="reaction_set")
async def set_reaction(interaction: discord.Interaction, role: discord.Role, category: str):
    """
    Добавляет реакцию на соответствующую роль

    :param interaction: Объект интерактива
    :param role: Роль на сервере
    :param category: Название категории, к которой крепится реакция
    """
    try:
        category_id = CategoryHandler().get(interaction.guild_id, category)[0][0]
        ReactionRoleHandler().edit(f"guild_id='{interaction.guild_id}' AND role_id='{role.id}'", category_id=category_id)
    except Exception as e:
        text = f'Упс... Что-то пошло не так.\nРазработчик скоро это починит.'
    else:
        text = f'Роль {role.mention} добавлена к категории **{category}**!'

    await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="reaction_delete")
async def delete(interaction: discord.Interaction, role: discord.Role):
    """
    Удаляет реакцию на соответствующей роли

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
