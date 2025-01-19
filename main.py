# Base packages
from dotenv import load_dotenv
import os

# Imports commands
from commands.roll import roll
from commands.initiative import initiative
from commands.stats import stats

# Loads utils
from utils.bot import bot
from utils.data_management import save_characters_to_file, load_characters_from_file

# Load environment variables from .env file
load_dotenv()

# Retrieve the Discord token and guild ID
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Error handling for missing token or guild ID
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables.")

# Load character data on bot startup
load_characters_from_file()

# Event to save character data when the bot shuts down
async def on_shutdown():
    save_characters_to_file()

# Run the bot
bot.run(DISCORD_TOKEN)
