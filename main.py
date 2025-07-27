import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

from events import setup_events
from commands import setup_commands
from reaction_roles import setup_reaction_events

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

if token is None:
    raise ValueError("DISCORD_TOKEN not set in .env file")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

setup_events(bot)
setup_commands(bot)
setup_reaction_events(bot)

bot.run(token, log_handler=handler, log_level=logging.INFO)