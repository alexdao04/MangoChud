import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Mango chudder {bot.user.name} has joined the chat!')

@bot.event
async def on_member_join(member):
    await member.send(f'Mango chudder {member.name} has joined the chat!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "akshant" in message.content.lower():
        await message.channel.send(f"{message.author.mention} - lower caste fremont indian detected")
    
    await bot.process_commands(message)

@bot.command()
async def chud(ctx):
    await ctx.send(f"Mango chudder {ctx.author.mention} is chudding in his goon cave as we speak!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name = "Rural Folk")
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} has been assigned the role {role.name}.")
    else:
        await ctx.send(f"Role {role.name} not found in this server.")

@bot.command()
async def unassign(ctx):
    role = discord.utils.get(ctx.guild.roles, name = "Rural Folk")
    if role in ctx.author.roles:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has been unassigned the role {role.name}.")
    else:
        await ctx.send(f"{ctx.author.mention} does not have the role {role.name}.")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)