import discord
import random
from bot import bot
from bot import GUILD_ID

# Predefined list of characters
character_list = ["Azalea", "Gorwick", "Globius", "Klud", "Mesmir", "Rogath"]

# Slash command to manage initiative
@bot.tree.command(name="initiative", description="Roll initiative and track turn order.", guild=GUILD_ID)
async def initiative(interaction: discord.Interaction, reset: bool = False, character: str = None):
    """
    Roll a d20 for initiative for the given character(s) or reset the tracker.
    """
    # Persistent tracker stored in memory
    if not hasattr(bot, "initiative_tracker"):
        bot.initiative_tracker = []

    # Handle reset
    if reset:
        bot.initiative_tracker = []
        await interaction.response.send_message("Initiative tracker has been reset.", ephemeral=True)
        return

    # Validate character input
    if character is None:
        await interaction.response.send_message("You must provide a character name unless resetting the tracker.", ephemeral=True)
        return

    # Handle "All" option
    if character == "All":
        # Add all characters to the initiative tracker
        for char in character_list:
            initiative_score = random.randint(1, 20)
            bot.initiative_tracker.append({"character": char, "initiative": initiative_score})
        # Sort the tracker
        bot.initiative_tracker = sorted(bot.initiative_tracker, key=lambda x: x["initiative"], reverse=True)
        # Generate tracker message
        tracker_message = "\n".join(
            [f"`{entry['character']}`: Initiative `{entry['initiative']}`" for entry in bot.initiative_tracker]
        )
        await interaction.response.send_message(
            f"Initiative rolled for all characters.\n\n**Current Initiative Order:**\n{tracker_message}"
        )
        return

    # Roll initiative for a single character
    initiative_score = random.randint(1, 20)
    if character not in [entry["character"] for entry in bot.initiative_tracker]:
        bot.initiative_tracker.append({"character": character, "initiative": initiative_score})
        bot.initiative_tracker = sorted(bot.initiative_tracker, key=lambda x: x["initiative"], reverse=True)

    # Generate tracker message
    tracker_message = "\n".join(
        [f"`{entry['character']}`: Initiative `{entry['initiative']}`" for entry in bot.initiative_tracker]
    )

    # Respond with the rolled result and updated tracker
    await interaction.response.send_message(
        f"`{character}` rolled initiative: 🎲 {initiative_score}\n\n**Current Initiative Order:**\n{tracker_message}"
    )
    
# Autocomplete for the `character` parameter
@initiative.autocomplete("character")
async def character_autocomplete(interaction: discord.Interaction, current: str):
    """
    Autocomplete for characters based on the predefined character list.
    """
    all_characters = character_list + ["All"]
    return [
        discord.app_commands.Choice(name=character, value=character)
        for character in all_characters
        if current.lower() in character.lower()
    ]
