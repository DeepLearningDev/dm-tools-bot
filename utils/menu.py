import discord
from utils.gen_roll import rng
from utils.bot import bot

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        
    @discord.ui.button(label="Roll initiative", style=discord.ButtonStyle.blurple)
    async def menu1(self, button: discord.ui.Button, interaction: discord.Interaction, output: str):
        await interaction.response.send_message(output)