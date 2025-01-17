import discord
import random
from bot import bot
from bot import GUILD_ID

# Slash command to roll a dice
@bot.tree.command(name="roll", description="Roll a dice from the D&D set.", guild=GUILD_ID)
async def roll(interaction: discord.Interaction, dice: str = None):
    """
    Roll a dice specified by the user (e.g., d20, d6) or roll a default d20 if not specified.
    """
    try:
        # Default dice if none is provided
        if dice is None:
            dice = "d20"
        
        # Validate the dice format (e.g., d20)
        if not dice.startswith("d") or not dice[1:].isdigit():
            await interaction.response.send_message("Invalid dice format! Use d4, d6, d8, d10, d12, or d20.", ephemeral=True)
            return
        
        sides = int(dice[1:])
        if sides not in [4, 6, 8, 10, 12, 20]:
            await interaction.response.send_message("Unsupported dice type! Use d4, d6, d8, d10, d12, or d20.", ephemeral=True)
            return
        
        # Roll the dice
        result = random.randint(1, sides)
        await interaction.response.send_message(f"You rolled a {dice}: 🎲 {result}")
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
        
# Specify choices for the `dice` parameter
@roll.autocomplete("dice")
async def dice_autocomplete(interaction: discord.Interaction, current: str):
    """
    Autocomplete for dice options (e.g., d4, d6, d8).
    """
    dice_options = ["d4", "d6", "d8", "d10", "d12", "d20"]
    return [
        discord.app_commands.Choice(name=dice, value=dice)
        for dice in dice_options
        if current.lower() in dice.lower()
    ]
