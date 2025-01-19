import discord
from utils.bot import bot
from utils.bot import GUILD_ID
from utils.stat_manager import get_character_stats

@bot.tree.command(name="stats", description="Get stats for a character.", guild=GUILD_ID)
async def stats(interaction: discord.Interaction, character: str, stat: str = None):
    """
    Retrieve stats for a character. Show all stats or a specific stat if provided.
    """
    character_stats = get_character_stats(character)
    if not character_stats:
        await interaction.response.send_message(f"Character '{character}' not found.", ephemeral=True)
        return

    if stat:
        # Return the specific stat
        if stat not in character_stats:
            await interaction.response.send_message(f"Stat '{stat}' not found for {character}.", ephemeral=True)
            return
        await interaction.response.send_message(f"{character}'s **{stat.capitalize()}**: {character_stats[stat]}")
    else:
        # Return all stats
        stats = "\n".join(
            [f"**{key.capitalize()}**: {value}" for key, value in character_stats.items() if key != "inventory"]
        )
        inventory = ", ".join(character_stats["inventory"]) if character_stats["inventory"] else "Empty"
        await interaction.response.send_message(
            f"**Stats for {character}:**\n{stats}\n\n**Inventory:** {inventory}"
        )

# Autocomplete for the `stat` parameter
@stats.autocomplete("stat")
async def stat_autocomplete(interaction: discord.Interaction, current: str):
    """
    Autocomplete for stat options based on the character.
    """
    character_name = interaction.namespace.character  # Get the character from the command
    character_stats = get_character_stats(character_name)
    if not character_stats:
        return []  # No suggestions if the character is not found

    return [
        discord.app_commands.Choice(name=key, value=key)
        for key in character_stats.keys()
        if current.lower() in key.lower() and key != "inventory"
    ]
