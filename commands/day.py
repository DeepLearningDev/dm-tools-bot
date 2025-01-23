import discord
from utils.bot import bot
from utils.bot import GUILD_ID
from utils.data_management import save_to_file

# Import the GM_ID from your environment
import os
GM_ID = os.getenv("GM_ID")

# Initialize the campaign day
Day = {"current_day": 1}

@bot.tree.command(name="day", description="Manage the campaign day.", guild=GUILD_ID)
async def day(
    interaction: discord.Interaction,
    action: str = "show",  # Default action is to show the current day
):
    """
    Display or advance the campaign day.
    """
    if action == "progress":
        # Allow only the GM to progress the day
        if str(interaction.user.id) != GM_ID:
            await interaction.response.send_message(
                "Only the GM can advance the campaign day.", ephemeral=True
            )
            return

        # Advance the day
        Day["current_day"] += 1
        save_to_file("savedata/day_log.json", Day)  # Save the updated day
        await interaction.response.send_message(
            f"A new day has dawned! The campaign is now on day {Day['current_day']}.", ephemeral=False
        )
    elif action == "show":
        # Display the current day
        await interaction.response.send_message(
            f"The campaign is currently on day {Day['current_day']}.", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "Invalid action. Use `show` to display the current day or `progress` to advance it (GM only).",
            ephemeral=True,
        )

# Autocomplete for the `action` parameter
@day.autocomplete("action")
async def day_action_autocomplete(interaction: discord.Interaction, current: str):
    """
    Autocomplete for day actions.
    """
    actions = ["show", "progress"]
    return [
        discord.app_commands.Choice(name=action, value=action)
        for action in actions
        if current.lower() in action.lower()
    ]
