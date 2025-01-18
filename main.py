from dotenv import load_dotenv
import os

# Loads file 
from commands.roll import roll
from commands.initiative import initiative
from utils.bot import bot

# Load environment variables from .env file
load_dotenv()

# Retrieve the Discord token and guild ID
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Error handling for missing token or guild ID
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables.")

# Run the bot
bot.run(DISCORD_TOKEN)
