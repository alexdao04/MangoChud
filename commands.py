import discord
from discord.ext import commands # pyright: ignore
from config import TRACKED_REACTION_MESSAGES, save_tracked_messages

def setup_commands(bot):
    
    @bot.command()
    async def react_to_assign(ctx):
        
        REACTION_EMOJI = {
            "👍": "thumbs_up",
        }

        REACTION_ROLE = {
            "thumbs_up": "Rural Folk",
        }

        message = await ctx.send("React to this message with a thumbs up to assign a role.")
        
        for reaction in REACTION_EMOJI.keys():
            await message.add_reaction(reaction)
        
        TRACKED_REACTION_MESSAGES[message.id] = {
            'emoji_map': REACTION_EMOJI,
            'role_map': REACTION_ROLE,
            'channel_id': ctx.channel.id,
            'guild_id': ctx.guild.id
        }
        
        save_tracked_messages(TRACKED_REACTION_MESSAGES)

    @bot.command()
    async def setup_reaction_role(ctx, message_id: int, emoji: str, *, role_name: str):
        try:
            message = None
            for channel in ctx.guild.text_channels:
                try:
                    message = await channel.fetch_message(message_id)
                    break
                except discord.NotFound:
                    continue
            
            if not message:
                await ctx.send(f"❌ Message with ID {message_id} not found in this server!")
                return
            
            await message.add_reaction(emoji)
            
            if message_id not in TRACKED_REACTION_MESSAGES:
                TRACKED_REACTION_MESSAGES[message_id] = {
                    'emoji_map': {},
                    'role_map': {},
                    'channel_id': message.channel.id,
                    'guild_id': ctx.guild.id
                }
            
            emoji_key = f"emoji_{len(TRACKED_REACTION_MESSAGES[message_id]['emoji_map'])}"
            TRACKED_REACTION_MESSAGES[message_id]['emoji_map'][emoji] = emoji_key
            TRACKED_REACTION_MESSAGES[message_id]['role_map'][emoji_key] = role_name
            
            save_tracked_messages(TRACKED_REACTION_MESSAGES)
            
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

    @bot.command()
    async def list_reaction_roles(ctx):
        if not TRACKED_REACTION_MESSAGES:
            await ctx.send("No reaction roles are currently set up.")
            return
        
        embed = discord.Embed(title="Tracked Reaction Role Messages", color=0x00ff00)
        
        for message_id, data in TRACKED_REACTION_MESSAGES.items():
            channel = bot.get_channel(data['channel_id'])
            channel_name = channel.name if channel else "Unknown Channel"
            
            role_list = []
            for emoji, emoji_key in data['emoji_map'].items():
                role_name = data['role_map'][emoji_key]
                role_list.append(f"{emoji} → {role_name}")
            
            embed.add_field(
                name=f"Message {message_id}",
                value=f"Channel: #{channel_name}\n" + "\n".join(role_list),
                inline=False
            )
        
        await ctx.send(embed=embed)