import discord # pyright: ignore
from discord.ext import commands # pyright: ignore
from config import TRACKED_REACTION_MESSAGES, save_tracked_messages # pyright: ignore

def setup_events(bot):
    
    @bot.event
    async def on_ready():
        print(f'Mango chudder {bot.user} is starting up!')

    @bot.event
    async def on_member_join(member):
        await member.send(f'Mango chudder {member.name} has joined the chat!')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        
        if "akshant" in message.content.lower():
            await message.channel.send(f"{message.author.mention} - lower caste fremont indian detected")

        if "chud" in message.content.lower():
            await message.channel.send(f"{message.author.mention} - mango chudder detected")

        await bot.process_commands(message)