import discord

from utils.gen_random import rng
from utils.bot import bot
from utils.bot import GUILD_ID

# Custom emojis for dice
dice_emojis = {
    4: "<:d4:1330649762386677850>", 
    6: "<:d6:1330649763569336390>", 
    8: "<:d8:1330649765385601094>", 
    10: "<:d10:1330649766761070663>", 
    12: "<:d12:1330649768145322099>", 
    20: "<:d20:1330649760658362500>"
}

# Slash command to roll a dice
@bot.tree.command(name="roll", description="Roll one or more dice with an optional modifier (e.g., 2d6+3).", guild=GUILD_ID)
async def roll(interaction: discord.Interaction, dice: str = None, modifier: int = 0):
    """
    Roll one or more dice specified by the user (e.g., 2d20, 4d6) with an optional modifier.
    """
    try:
        # Default dice if none is provided
        if dice is None:
            dice = "1d20"
        
        # Parse the dice string (e.g., "2d6")
        if "d" not in dice or not dice.replace("d", "").replace("+", "").isdigit():
            await interaction.response.send_message("Invalid dice format! Use XdY (e.g., 2d6, d20).", ephemeral=True)
            return
        
        # Split the dice string into the number of dice and sides (e.g., "2d6" -> 2, 6)
        parts = dice.split("d")
        num_dice = int(parts[0]) if parts[0] else 1  # Default to 1 die if not specified
        sides = int(parts[1])

        if sides not in dice_emojis:
            await interaction.response.send_message("Unsupported dice type! Use d4, d6, d8, d10, d12, or d20.", ephemeral=True)
            return

        if num_dice <= 0 or num_dice > 100:
            await interaction.response.send_message("Please roll between 1 and 100 dice.", ephemeral=True)
            return

        # Roll the dice
        rolls = [rng(sides) for _ in range(num_dice)]
        total_result = sum(rolls) + modifier

        # Get the appropriate dice emoji
        dice_emoji = dice_emojis[sides]

        # Format the response
        breakdown = ", ".join(map(str, rolls))  # List of rolls
        if not modifier == 0:
            output1 = f"You rolled {dice} {dice_emoji} with a modifier of {modifier}\n"
            output2 = f"Your rolls: `{breakdown}` → Total: **{total_result}**  |  {total_result - modifier} + {modifier}"
            output = output1 + output2
        elif num_dice > 1:
            output1 = f"You rolled {dice} {dice_emoji}\n"
            output2 = f"Your rolls: `{breakdown}` → Total: **{total_result}**"
            output = output1 + output2
        else:
            output1 = f"You rolled {dice} {dice_emoji}\n"
            output2 = f"Your roll: **{breakdown}**"
            output = output1 + output2
            
        response = (
            f"{output}\n"
        )

        await interaction.response.send_message(response)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

# Specify choices for the `dice` parameter
@roll.autocomplete("dice")
async def dice_autocomplete(interaction: discord.Interaction, current: str):
    """
    Autocomplete for dice options (e.g., d4, d6, d8).
    """
    dice_options = ["1d4", "2d4", "3d4", "1d6", "2d6", "3d6", "1d8", "2d8", "1d10", "2d10", "1d12", "1d20", "2d20"]
    return [
        discord.app_commands.Choice(name=dice, value=dice)
        for dice in dice_options
        if current.lower() in dice.lower()
    ]
