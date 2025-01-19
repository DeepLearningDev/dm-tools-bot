import discord
from utils.gen_roll import rng
from utils.bot import bot
from utils.bot import GUILD_ID

# Custom emojis for dice
dice_emojis = {
    4: "<:d4:1330394292308541440>", 
    6: "<:d6:1330394298197348433>", 
    8: "<:d8:1330394299996704889>", 
    10: "<:d10:1330394301334683708>", 
    12: "<:d12:1330394302471475200>", 
    20: "<:d20:1330394303402344551>"
}

# Slash command to roll a dice
@bot.tree.command(name="roll", description="Roll a dice from the D&D set, optionally with a modifier.", guild=GUILD_ID)
async def roll(interaction: discord.Interaction, dice: str = None, modifier: int = None):
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
        if sides not in dice_emojis:
            await interaction.response.send_message("Unsupported dice type! Use d4, d6, d8, d10, d12, or d20.", ephemeral=True)
            return

        # Roll the dice
        roll_result = rng(sides)
        total_result = roll_result + (modifier if modifier else 0)

        # Get the appropriate dice emoji
        dice_emoji = dice_emojis[sides]

        # Format the response
        if modifier is not None:
            response = (
                f"You rolled a {dice} {dice_emoji} **{total_result}**\n"
                f"Breakdown: ({roll_result}) + {modifier} = **{total_result}**"
            )
        else:
            response = f"You rolled a {dice} {dice_emoji} **{roll_result}**"

        await interaction.response.send_message(response)
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
