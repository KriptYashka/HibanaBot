import discord
from discord import ui


class SettingRoleView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label='Настроить',
               style=discord.ButtonStyle.primary)
    async def btn_start(self, interaction: discord.Interaction, button: discord.ui.Button):
        if isinstance(interaction.user, discord.Member):
            if interaction.user.top_role.permissions.administrator:
                text = 'Щя будем настраивать роли, юху!'
                button.label = "Настройка"
                button.disabled = True
                self.btn_pass.disabled = None
                await interaction.response.edit_message(content=text, view=self)
            else:
                text = f'Настраивать может только администратор.\n' \
                       f'Пожалуйста, не мешайте ему, {interaction.user.mention}!'
                await interaction.user.send(text)

    @ui.button(label='Пропустить',
               style=discord.ButtonStyle.secondary)
    async def btn_pass(self, interaction: discord.Interaction, button: discord.ui.Button):
        if isinstance(interaction.user, discord.Member):
            if interaction.user.top_role.permissions.administrator:
                text = f":x:Настройка ролей отменена"
                button.view.clear_items()
                await interaction.response.edit_message(content=text, view=self)
                await interaction.message.delete(delay=3)

    @ui.select(cls=discord.ui.RoleSelect,
               placeholder="Какую роль можно получить участникам сервера?",
               min_values=1, max_values=20)
    async def select_roles(self, interaction: discord.Interaction, select: discord.ui.RoleSelect):
        text = f"**Выбранные роли:** \n"
        for role in select.values:
            text += f"- {role.name}\n"
        text += f"\nВведите реакции в строчку соответственно порядку ролей (количество - {len(select.values)})"

        await interaction.response.edit_message(content=text)