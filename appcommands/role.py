from typing import List, Optional

import discord
from discord import app_commands as ac
import emoji

import permission
from handlers.select_role_hand import ReactionRoleHandler, CategoryHandler, CategoryMessageHandler

role_permission = permission.guild.is_admin


@ac.command(name="reaction_add")
@role_permission()
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
        text = f'❌Роль {role.mention} ({db_role[0][4]}) уже существует. Выберите другую роль.'
        return await interaction.response.send_message(content=text, ephemeral=True)
    emojis_str = [str(item) for item in interaction.guild.emojis]
    if not (emoji.is_emoji(emoji_str) or emoji_str in emojis_str):
        text = f'❌Реакция ({emoji_str}) не является стандартным эмоджи. Выберите другую реакцию.'
        return await interaction.response.send_message(content=text, ephemeral=True)

    ReactionRoleHandler().add(guild_id=interaction.guild_id, role_id=role.id, emoji=emoji_str)
    text = f'Роль {role.mention} ({emoji_str}) успешно добавлена в систему ролей вашего сервера.'
    await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="reaction_show")
@role_permission()
async def show(interaction: discord.Interaction, only_free: bool = False):
    """
    Показывает все роли с реакциями и в каких категориях их можно получить

    :param interaction: Объект интерактива
    :param only_free: Отображение только свободных ролей
    """
    h_category = CategoryHandler()
    h_role = ReactionRoleHandler()

    roles = h_role.select(f"guild_id={interaction.guild_id} AND category is NULL")
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
        embed = h_category.get_embed_show(category, interaction.guild)
        roles = h_role.select(f"guild_id={interaction.guild_id} AND category='{category[1]}'")
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
@role_permission()
async def set_reaction(interaction: discord.Interaction, role: str, category: str):
    """
    Прикрепляет роль-реакцию к категории

    :param interaction: Объект интерактива
    :param role: Название роли на сервере
    :param category: Название категории, к которой крепится реакция
    """
    if not (category_data := CategoryHandler().get(interaction.guild_id, category)):
        text = f"❌Категории {category} не существует на данном сервере."
        return await interaction.response.send_message(content=text, ephemeral=True)
    if not role[2:-1].isdecimal():
        return await interaction.response.send_message(content=f'❌Неверно введены данные роли.', ephemeral=True)
    role = interaction.guild.get_role(int(role))
    ReactionRoleHandler().edit(f"guild_id='{interaction.guild_id}' AND role_id='{role.id}'",
                               category=category_data[1])
    role_data = ReactionRoleHandler().get(interaction.guild_id, role.id)
    await change_category_msg_reaction_set(interaction, category, role_data[4])
    text = f'Роль {role.mention} добавлена к категории **{category}**!'
    await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="reaction_unset")
@role_permission()
async def unset_reaction(interaction: discord.Interaction, role: str):
    """
    Убирает роль-реакцию с категории

    :param interaction: Объект интерактива
    :param role: Роль на сервере
    :param category: Название категории, от которой открепляется реакция
    """
    if not role[2:-1].isdecimal():
        return await interaction.response.send_message(content=f'Неверно введены данные роли.', ephemeral=True)
    h_role = ReactionRoleHandler()
    role = interaction.guild.get_role(int(role))
    where_expr = f"guild_id='{interaction.guild_id}' AND role_id='{role.id}'"
    if reaction := h_role.select(where_expr):
        reaction = reaction[0]
        h_role.edit(where_expr, category="NULL")
        await change_category_msg_reaction_unset(interaction, reaction[3], reaction[4])

        text = f'Роль {role.mention} убрана с категории **{reaction[3]}**!'
    else:
        text = f'❌Роль {role.mention} не была прикреплена ранее.'
    await interaction.response.send_message(content=text, ephemeral=True)


@ac.command(name="reaction_delete")
@role_permission()
async def delete(interaction: discord.Interaction, role: str):
    """
    Удаляет реакцию с соответствующей роли

    :param interaction: Объект интерактива
    :param role: Роль на сервере
    """

    h_role = ReactionRoleHandler()
    if not role[2:-1].isdecimal():
        return await interaction.response.send_message(content=f'Неверно введены данные роли.', ephemeral=True)
    role = interaction.guild.get_role(int(role))
    reaction = h_role.get(interaction.guild_id, role.id)
    if is_exist := h_role.delete(guild_id=interaction.guild_id, role_id=role.id):
        await change_category_msg_reaction_unset(interaction, reaction[3], reaction[4])
        text = f'Роль {role.mention} исключена из системы получения ролей.'
    else:
        text = f"❌Роль {role.mention} не привязана. В текущий момент она не была добавлена в систему получения ролей."
    await interaction.response.send_message(content=text, ephemeral=True)


async def change_category_msg_reaction_set(interaction: discord.Interaction, category_title: str, emoji_add: str):
    """
    Редактирует сообщения категорий на сервере. Добавляет прикрепленные реакции к сообщению.
    """
    h_category_msg = CategoryMessageHandler()
    h_role = ReactionRoleHandler()
    if category_msg := h_category_msg.get_guild_category_msg(interaction.guild_id, category_title):
        discord_msg = await h_category_msg.get_discord_msg_by_data(interaction, category_msg)
        await discord_msg.add_reaction(emoji_add)
        if embeds := discord_msg.embeds:
            embed = embeds[0]
            roles = h_role.get(interaction.guild_id, category_title=category_title)
            text = f"{len(roles)} ролей"
            for role_db in roles:
                role_discord = interaction.guild.get_role(role_db[2])
                text += f"\nРоль {role_discord.mention} - {role_db[4]}"
                embed.remove_field(0)
                embed.add_field(name="Доступны следующие роли", value=text)
                await discord_msg.edit(embeds=embeds)


async def change_category_msg_reaction_unset(interaction: discord.Interaction, category_title: str, emoji_deleted: str):
    """
    Редактирует сообщения категорий на сервере. Убирает открепленные / удаленные реакции в содержимом сообщения.
    """
    h_category_msg = CategoryMessageHandler()
    if category_msg := h_category_msg.get_guild_category_msg(interaction.guild_id, category_title):
        discord_msg = await h_category_msg.get_discord_msg_by_data(interaction, category_msg)
        await discord_msg.clear_reaction(emoji_deleted)
        if embeds := discord_msg.embeds:
            embed = embeds[0]
            for index, field in enumerate(embeds[0].fields):
                if field.name == "Доступны следующие роли":  # TODO: Выглядит, как костыль
                    new_rows = [row for row in field.value.split("\n") if row.count(emoji_deleted) == 0]
                    text = "\n".join(new_rows) if new_rows else "У данной категории нет ролей. Она. Просто. Существует."
                    embed.remove_field(index)
                    embed.add_field(name=field.name, value=text, inline=field.inline)
                    await discord_msg.edit(embed=embed)
