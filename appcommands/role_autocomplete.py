from typing import List

import discord
from discord import app_commands as ac

from appcommands.role import set_reaction, unset_reaction, delete
from select_role_hand import ReactionRoleHandler
from handlers.select_role_hand import CategoryHandler


@set_reaction.autocomplete('category')
async def category_autocomplete(interaction: discord.Interaction, current: str) -> List[ac.Choice[str]]:
    categories = CategoryHandler().get(interaction.guild_id)
    if not categories:
        return []
    categories_name = [category[1] for category in categories]
    return [
        ac.Choice(name=name, value=name) for name in categories_name if current.lower() in name.lower()
    ]


@unset_reaction.autocomplete('role')
async def role_str_autocomplete(interaction: discord.Interaction, current: str) -> List[ac.Choice[str]]:
    if not (db_roles := ReactionRoleHandler().get(interaction.guild_id)):
        return []
    db_role_ids = {role[2]: role[3] for role in db_roles if role[3]}
    return await get_choice_role(interaction, db_role_ids, current)


@delete.autocomplete('role')
async def role_str_autocomplete(interaction: discord.Interaction, current: str) -> List[ac.Choice[str]]:
    if not (db_roles := ReactionRoleHandler().get(interaction.guild_id)):
        return []
    db_role_ids = {role[2]: role[3] for role in db_roles}
    return await get_choice_role(interaction, db_role_ids, current)


async def get_choice_role(interaction: discord.Interaction, db_role_ids: dict, current: str):
    role_names = []
    for i, role in enumerate(interaction.guild.roles):
        if role.id in db_role_ids:
            item = [f"[{db_role_ids[role.id]}] {role.name}", role.id]
            role_names.append(item)
    return [
        ac.Choice(name=name, value=str(i)) for name, i in role_names if current.lower() in name.lower()
    ]


def main():
    print("Новый файл, юху!")


if __name__ == "__main__":
    main()


@set_reaction.autocomplete('role')
async def role_str_autocomplete(interaction: discord.Interaction, current: str) -> List[ac.Choice[str]]:
    if not (db_roles := ReactionRoleHandler().get(interaction.guild_id)):
        return []
    db_role_ids = [role[2] for role in db_roles if not role[3]]
    role_names = [(role.name, str(role.id)) for role in interaction.guild.roles if role.id in db_role_ids]
    return [
        ac.Choice(name=name, value=i) for name, i in role_names if current.lower() in name.lower()
    ]
