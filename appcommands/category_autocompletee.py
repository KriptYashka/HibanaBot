from typing import List

import discord
from discord import app_commands as ac

from appcommands.category import edit, show, create, delete, set_reaction
from handlers.select_role_hand import CategoryHandler


@edit.autocomplete('title')
@show.autocomplete('title')
@create.autocomplete('title')
@delete.autocomplete('title')
@set_reaction.autocomplete('category')
async def category_autocomplete(interaction: discord.Interaction, current: str) -> List[ac.Choice[str]]:
    categories = CategoryHandler().get(interaction.guild_id)
    if not categories:
        return []
    categories_name = [category[1] for category in categories]
    return [
        ac.Choice(name=name, value=name) for name in categories_name if current.lower() in name.lower()
    ]

def main():
    print("Новый файл, юху!")


if __name__ == "__main__":
    main()
