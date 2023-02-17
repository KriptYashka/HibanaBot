from typing import List, Union

import discord
from discord.ext import commands
from discord import ui
from interactions.modal_example import Text


class SettingRoleView(ui.View):
    @staticmethod
    async def check_member_admin(interaction: discord.Interaction) -> bool:
        if not isinstance(interaction.user, discord.Member):
            return False

        if not interaction.user.top_role.permissions.administrator:
            text = f'Настраивать может только администратор.\n' \
                   f'Пожалуйста, не мешайте ему, {interaction.user.mention}!'
            await interaction.user.send(text)
            return False

        return True

    def __init__(self):
        super().__init__(timeout=30)
        self.set_items([self.btn_start, self.btn_pass])

    def set_items(self, items: List[ui.Item]):
        self.clear_items()
        for item in items:
            self.add_item(item)

    @ui.button(label='Настроить',
               style=discord.ButtonStyle.primary)
    async def btn_start(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not SettingRoleView.check_member_admin(interaction):
            return None

        text = 'Щя будем настраивать роли, юху!'

        self.set_items([self.select_roles])
        return await interaction.response.edit_message(content=text, view=self)

    @ui.button(label='Пропустить',
               style=discord.ButtonStyle.secondary)
    async def btn_pass(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not SettingRoleView.check_member_admin(interaction):
            return None

        text = f":x:Настройка ролей отменена"

        self.clear_items()
        await interaction.response.edit_message(content=text, view=self)
        await interaction.message.delete(delay=3)

    @ui.select(cls=discord.ui.RoleSelect,
               placeholder="Какую роль можно получить участникам сервера?",
               min_values=1, max_values=20)
    async def select_roles(self, interaction: discord.Interaction, select: discord.ui.RoleSelect):
        if not SettingRoleView.check_member_admin(interaction):
            return None

        text = f'**Выбранные роли:** \n'
        for role in select.values:
            text += f"- {role.name}\n"
        text += f"\nВведите реакции в строчку соответственно порядку ролей (количество - {len(select.values)})"

        await interaction.response.send_modal(content=text, view=Text)
