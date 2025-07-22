# MangoChud v0.1: A bot originally conceived for the Mango Chudney discord server.
# This bot is a general-purpose server bot for moderation, role assignment, fun interactions, and more.

# I built this bot using the discord.py library, a Python wrapper that makes Discord API calls easy.
# This bot is by "Alexander Dao" (me), and is open source under MIT license.

# import main.py packages
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

if token is None: # ValueError does the same thing a try except or assert would do, but in less lines
    raise ValueError("DISCORD_TOKEN not set in .env file") # raises an error when our .env file isn't set up
# probably not the best way to do this, but the interpreter and the framework was bitching about it
# so we just catch the error like patching flex tape on a leaking boat

# this logs messages to a file called discord.log
# logs bot activity, errors, etc (probably not gonna touch this for now)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# intents give the bot permission to do stuff (we handle this on the discord developer portal)
# that makes it like 1000x easier to manage permissions rather than handling it in back end code
# this is the bot object, which is the main interface for interacting with the discord API
# we set the command prefix to '/' so that we can use commands like /assign, /
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready(): # just a startup message for when we run the bot
    print(f'Mango chudder {bot.user} is starting up!')

@bot.event # when someone joins the server.
async def on_member_join(member):
    await member.send(f'Mango chudder {member.name} has joined the chat!')

@bot.event
async def on_message(message): # fun message handler, reads messages for keywords
    if message.author == bot.user: # if the message is from the bot itself, we ignore it
        return # this prevents the bot from looping its own messages
    
    if "akshant" in message.content.lower(): # inside joke, sorry akshant you're the homie though
        await message.channel.send(f"{message.author.mention} - lower caste fremont indian detected")
        # neil's reaction told me everything i needed to know
        # so we made it for real lol

    if "chud" in message.content.lower():
        await message.channel.send(f"{message.author.mention} - mango chudder detected")
        # this replaces the chud command, which is honestly kind of useless
        # just a cool way to test this framework out, but we can save the commands for more essential things

    await bot.process_commands(message)
    # i dont know the deeper workings of this framework, but calling process_commands
    # calls a premade function that processes any speech containing this keyword
    # the reaction role message id, which is a message that has a reaction role
    # is hardcoded here, so if you change the message id, you need to change it here too

# this is where the commands are defined. we're going to structure this in a way
# that we can find everything easily when we need to edit it later.
# admittedly, i'm tempted to set the main.py up so that it jumps to other files
# e.g. commands.py, events.py, etc. but for now, we keep this in one file until the need arises

# TODO: what we want to do here is assign a role to a user when they react to a message
# treat it like it's integrated into the server at the moment as a functionality (and left in main.py)
# but when this bot is expanded to work on multiple servers, we can move this to a separate file
@bot.command()
async def assign_role_when_reacted(ctx):
    """
    Sends a message prompting the user to react with a thumbs up emoji,
    and assigns the corresponding role based on the reaction.
    Usage: /assign_role_when_reacted
    """
    
    REACTION_ROLES = {
        "👍": "thumbs_up",
    }

    message = await ctx.send("React to this message with a thumbs up to assign a role.")
    # if the number of reactions grows, consider batching or optimizing this process for better performance.
    for reaction in REACTION_ROLES.keys():
        await message.add_reaction(reaction)
        # i'm surprised it's that simple, but that's what the wrapper does..
        # i'm curious how the api calls work under the hood. thats what i hate about python
        # it makes things easier to use, but you dont actually understand what's happening

    def reaction_check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in REACTION_ROLES
    # this is a check to see if the reaction is from the user who sent the command
    try:
        role_name = REACTION_ROLES[str(reaction.emoji)]
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            try:
                await ctx.author.add_roles(role)
                await ctx.send(f"{ctx.author.mention} has been assigned the role {role.name}.")
            except discord.Forbidden:
                logging.error(f"Bot lacks permission to assign role '{role_name}' to {ctx.author}.")
                await ctx.send(f"Sorry, I don't have permission to assign the role {role.name}.")
            except Exception as e:
                logging.error(f"Error assigning role '{role_name}' to {ctx.author}: {e}")
                await ctx.send(f"An error occurred while assigning the role {role.name}.")
        else:
            logging.warning(f"Role '{role_name}' not found in server '{ctx.guild.name}'.")
            await ctx.send(f"Role {role_name} not found in this server.")
            await ctx.send(f"Role {role_name} not found in this server.")
    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention}, you took too long to react! Please try again.")

# NOTE: THESE COMMANDS ARE THE GENERAL COMMANDS FOR THIS BOT
@bot.command()
async def assign(ctx): # self-explanatory, this command assigns a basic role for a user
    # the user can assign this role without any permissions being needed
    # basic implementation, we can expand on this slightly later
    role = discord.utils.get(ctx.guild.roles, name = "Rural Folk")
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} has been assigned the role {role.name}.")
    else:
        await ctx.send(f"Role {role.name} not found in this server.")

@bot.command()
async def unassign(ctx): # self-explanatory, this command unassigns a basic role for a user
    # in it's most basic form, the user can remove their role without any permissions
    role = discord.utils.get(ctx.guild.roles, name = "Rural Folk")
    if role in ctx.author.roles:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has been unassigned the role {role.name}.")
    else:
        await ctx.send(f"{ctx.author.mention} does not have the role {role.name}.")

bot.run(token, log_handler=handler, log_level=logging.INFO)
# we run the bot at the end with the env file token
# after we've defined all our events and commands that this bot should support
