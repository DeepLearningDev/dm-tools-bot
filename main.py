# Base packages
from dotenv import load_dotenv
import os
import signal
import asyncio

# Imports commands
from commands.roll import roll
from commands.initiative import initiative
from commands.stats import stats

# Loads utils
from utils.bot import bot
from utils.data_management import save_characters_to_file, load_characters_from_file

# Load environment variables from .env file
load_dotenv()

# Retrieve the Discord token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Error handling for missing token
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables.")

# Load character data on bot startup
load_characters_from_file()

# Function to handle graceful shutdown
def graceful_shutdown():
    print("Shutting down bot and saving data...")
    save_characters_to_file()
    # Close the event loop
    asyncio.get_event_loop().stop()

# Register shutdown signals
signal.signal(signal.SIGINT, lambda signum, frame: graceful_shutdown())
signal.signal(signal.SIGTERM, lambda signum, frame: graceful_shutdown())

# Run the bot
bot.run(DISCORD_TOKEN)
