import discord
from discord.ext import commands
from models.db.reaction_msg import MessageReaction, SettingRole


class SettingRoleDecideView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Настроить', style=discord.ButtonStyle.primary)
    async def btn_start(self, interaction: discord.Interaction, button: discord.ui.Button):
        if isinstance(interaction.user, discord.Member):
            if interaction.user.top_role.permissions.administrator:
                text = 'Щя будем настраивать роли, юху!'
                button.label = "Настройка"
                button.disabled = True
                self.btn_pass.disabled = None
                await interaction.response.edit_message(content=text, view=DampingView())
            else:
                await interaction.response.defer()
                text = f'Настраивать может только администратор.\n' \
                       f'Пожалуйста, не мешайте ему, {interaction.user.mention}!'
                await interaction.user.send(text)

    @discord.ui.button(label='Пропустить', style=discord.ButtonStyle.secondary)
    async def btn_pass(self, interaction: discord.Interaction, button: discord.ui.Button):
        if isinstance(interaction.user, discord.Member):
            if interaction.user.top_role.permissions.administrator:
                text = f":x:Настройка ролей отменена"
                button.view.clear_items()
                await interaction.response.edit_message(content=text, view=self)
                await interaction.message.delete(delay=3)


class DampingView(discord.ui.View):

    def __init__(self):
        super().__init__()

    @discord.ui.select(cls=discord.ui.RoleSelect,
                       placeholder="Какую роль можно получить участникам сервера?",
                       min_values=1, max_values=20)
    async def select_roles(self, interaction: discord.Interaction, select: discord.ui.RoleSelect):
        text = f"**Выбранные роли:** \n"
        for role in select.values:
            text += f"- {role.name}\n"
        text += f"\nВведите реакции в строчку соответственно порядку ролей (количество - {len(select.values)})"
        # await interaction.response.edit_message(content=text)
        await interaction.response.send_modal(Text())


class Text(discord.ui.Modal, title='Questionnaire Response'):
    name = discord.ui.TextInput(label='Name')
    answer = discord.ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)


class SettingRoleView(discord.ui.View):

    def __init__(self):
        super().__init__()

    @discord.ui.select(cls=discord.ui.RoleSelect,
                       placeholder="Какую роль можно получить участникам сервера?",
                       min_values=1, max_values=20)
    async def select_roles(self, interaction: discord.Interaction, select: discord.ui.RoleSelect):
        role = select.values[0]
        return await interaction.response.send_message(f'You selected {role.mention}')


async def msg_roles(bot: commands.Bot, msg: discord.Message) -> discord.Message:
    """
    Обработчик выдачи сообщения типа "реакции-роли"

    :param bot: discord-бот
    :param msg: сообщение-запрос от пользователя
    :return: отправленное сообщение о статусе операции
    """
    await msg.delete()
    if not (setting_roles := SettingRole().get(msg.guild.id)):
        text = f'Не настроены роли для сервера'
        view = SettingRoleDecideView()
        delay = None
        if not (is_admin := msg.author.top_role.permissions.administrator):
            text += "\n*Задать настройки могут администраторы сервера.*"
            delay = 5
            view = None

        return await msg.channel.send(text, view=view, delete_after=delay)

    if old_msg_id := MessageReaction().get_msg_id(msg.guild.id):
        return await msg.channel.send(f"Уже существует сообщение с ролями:\n"
                                      f"https://discord.com/channels/{msg.guild.id}/{msg.channel.id}/{old_msg_id}")

    return await send_msg_roles(msg, setting_roles)


async def send_msg_roles(msg: discord.Message, setting: dict[str, int], text: str = None) -> discord.Message:
    """
    Отправляет сообщение с реакциями-ролями.

    :param text: текст сообщения с реакциями-ролями
    :param msg: сообщение-запрос от пользователя
    :param setting: настройки сервера реакции-роли
    :return: отправленное сообщение о статусе операции
    """
    text = text if text else "Give roles"
    new_msg = await msg.channel.send(text)
    if new_msg:
        MessageReaction().add(new_msg)
        for emoji in setting:
            await new_msg.add_reaction(emoji)
    return new_msg


def is_role_message(message_id: int) -> bool:
    """
    Является ли сообщение вида "реакция-роль".

    :param message_id: id сообщения
    :return: True или False
    """
    return MessageReaction().is_exist_msg(message_id)


def get_setting_roles(guild_id):
    """
    Возвращает настройки сервера "реакции-роли"

    :param guild_id: id сервера
    :return: настройки сервера "реакции-роли"
    """
    return SettingRole().get(guild_id)


def check_msg_delete(msg_id: int, guild_id: int):
    db = MessageReaction()
    if msg_id == db.get_msg_id(guild_id):
        db.delete("id", msg_id)
