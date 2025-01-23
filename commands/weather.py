import discord

from utils.bot import bot
from utils.bot import GUILD_ID
from utils.gen_random import random_weather

@bot.tree.command(name="weather", description="Generate random weather.", guild=GUILD_ID)
async def weather(interaction: discord.Interaction, type: str = None, region: str = None):
    """
    Generate weather, either completely random, type-specific, or region-specific.
    """
    weather_condition = random_weather(type=type, region=region)
    await interaction.response.send_message(f"The generated weather is: **{weather_condition}**")

@weather.autocomplete("type")
async def weather_type_autocomplete(interaction: discord.Interaction, current: str):
    """
    Autocomplete for weather types.
    """
    weather_types = ["general", "hot", "cold", "wet", "dry", "windy"]
    return [
        discord.app_commands.Choice(name=weather_type, value=weather_type)
        for weather_type in weather_types
        if current.lower() in weather_type.lower()
    ]

@weather.autocomplete("region")
async def weather_region_autocomplete(interaction: discord.Interaction, current: str):
    """
    Autocomplete for regions.
    """
    regions = ["mountain", "desert", "swamp", "forest", "plains", "coast"]
    return [
        discord.app_commands.Choice(name=region, value=region)
        for region in regions
        if current.lower() in region.lower()
    ]
