import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

GUILD_ID = os.getenv('GUILD_ID')
if not GUILD_ID:
    raise ValueError("GUILD_ID not found in environment variables.")

GUILD_ID = discord.Object(id=GUILD_ID)

# Define the bot's client class
class Client(commands.Bot):
    async def on_ready(self):
        print(f'{self.user} is now online!')

        try:
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f'Synced {len(synced)} commands to server {GUILD_ID.id}')
            print(f'Registered commands: {[cmd.name for cmd in self.tree.get_commands(guild=GUILD_ID)]}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

# Define the bot's intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with command prefix and intents
bot = Client(command_prefix="!", intents=intents)