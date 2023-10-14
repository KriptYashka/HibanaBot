import discord
from discord import app_commands


def is_admin():
    def predicate(interaction: discord.Interaction):
        return interaction.user.guild_permissions.administrator

    return app_commands.check(predicate)


def is_staff():
    def predicate(interaction: discord.Interaction):
        return interaction.user.guild_permissions.manage_roles

    return app_commands.check(predicate)


def is_owner():
    def predicate(interaction: discord.Interaction):
        return interaction.user.id == interaction.guild.owner_id

    return app_commands.check(predicate)


def is_moderator():
    def predicate(interaction: discord.Interaction):
        return interaction.user.guild_permissions.manage_channels

    return app_commands.check(predicate)


def is_owner_or_moderator():
    def predicate(interaction: discord.Interaction):
        return interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_channels

    return app_commands.check(predicate)


def main():
    print("Новый файл, юху!")


if __name__ == "__main__":
    main()
