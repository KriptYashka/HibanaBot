import discord
from discord import ui


class Text(ui.Modal, title='Настройка реакций для ролей'):
    name = ui.TextInput(label='Name')

    async def on_submit(self, interaction: discord.Interaction):
        self.name = None
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)
