import discord

from utils.bot import bot
from utils.bot import GUILD_ID

from utils.stat_manager import get_character_stats
from commands.initiative import character_ids, character_list, GM_ID


@bot.tree.command(name="stats", description="Get stats for a character.", guild=GUILD_ID)
async def stats(interaction: discord.Interaction, character: str, stat: str = None):
    """
    Retrieve stats for a character. Show all stats or a specific stat if provided.
    """
    user_id = str(interaction.user.id)
    character_index = None

    # Check if the user is allowed to access the stats
    if user_id != GM_ID:
        if character not in character_list:
            await interaction.response.send_message(f"Character '{character}' not found.", ephemeral=True)
            return

        character_index = character_list.index(character)
        assigned_user_id = character_ids[character_index]

        if user_id != assigned_user_id:
            await interaction.response.send_message(
                "You do not have permission to view stats for this character.", ephemeral=True
            )
            return

    # Fetch character stats
    character_stats = get_character_stats(character)
    if not character_stats:
        await interaction.response.send_message(f"Character '{character}' not found.", ephemeral=True)
        return

    if stat:
        # Return the specific stat
        if stat not in character_stats:
            await interaction.response.send_message(f"Stat '{stat}' not found for {character}.", ephemeral=True)
            return
        await interaction.response.send_message(
            f"{character}'s **{stat.capitalize()}**: {character_stats[stat]}", ephemeral=True
        )
    else:
        # Group stats, mods, and saves
        stats_table = "```\n"  # Start a code block
        stats_table += f"Stats for {character}:\n"
        stats_table += f"{'Attribute':<12} | {'Stat':<5} | {'Mod':<5} | {'Save':<5}\n"
        stats_table += "-" * 38 + "\n"  # Separator
        attributes = ["str", "dex", "const", "int", "wis", "chr"]
        for attr in attributes:
            stat = character_stats.get(attr, "N/A")
            mod = character_stats.get(f"{attr}_mod", "N/A")
            save = character_stats.get(f"{attr}_save", "N/A")
            stats_table += f"{attr.capitalize():<12} | {stat:<5} | {mod:<5} | {save:<5}\n"

        stats_table += "```\n"

        # Add other stats (non-attribute-related)
        other_stats = "\n".join(
            [f"**{key.capitalize()}**: {value}" for key, value in character_stats.items()
             if key not in attributes and not key.endswith(("_mod", "_save")) and key != "inventory"]
        )

        # Inventory
        inventory = ", ".join(character_stats["inventory"]) if character_stats["inventory"] else "Empty"

        await interaction.response.send_message(
            f"{stats_table}\n**Other Stats:**\n{other_stats}\n\n**Inventory:** {inventory}", ephemeral=True
        )


# Autocomplete for the `character` parameter
@stats.autocomplete("character")
async def character_autocomplete(interaction: discord.Interaction, current: str):
    """
    Autocomplete for character names based on the input.
    """
    return [
        discord.app_commands.Choice(name=character, value=character)
        for character in character_list
        if current.lower() in character.lower()
    ]


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
        if current.lower() in key.lower()
    ]
