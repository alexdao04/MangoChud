import discord
from config import TRACKED_REACTION_MESSAGES, save_tracked_messages

def setup_reaction_events(bot):
    @bot.event
    async def on_reaction_add(reaction, user):
        if user.bot:
            return

        message_id = reaction.message.id
        if message_id not in TRACKED_REACTION_MESSAGES:
            return

        tracked_data = TRACKED_REACTION_MESSAGES[message_id]
        emoji_str = str(reaction.emoji)

        possible_emoji_keys = [
            emoji_str,
            str(reaction.emoji),
            reaction.emoji.name if hasattr(reaction.emoji, 'name') else None,
            '👍',
            '\U0001f44d',
            '\ud83d\udc4d',
        ]

        emoji_key = None
        for possible_key in possible_emoji_keys:
            if possible_key and possible_key in tracked_data['emoji_map']:
                emoji_key = tracked_data['emoji_map'][possible_key]
                break

        if not emoji_key or emoji_key not in tracked_data['role_map']:
            return

        role_name = tracked_data['role_map'][emoji_key]
        guild = reaction.message.guild
        role = discord.utils.get(guild.roles, name=role_name)

        if not role:
            await reaction.message.channel.send(f"❌ Role **{role_name}** not found in this server!")
            return

        if role in user.roles:
            await reaction.message.channel.send(f"ℹ️ {user.mention} already has the **{role.name}** role!")
            return

        if guild.me.top_role.position <= role.position:
            await reaction.message.channel.send(f"❌ My role is not high enough to assign the **{role.name}** role!")
            return

        try:
            await user.add_roles(role)
            await reaction.message.channel.send(f"✅ {user.mention} has been assigned the **{role.name}** role!")
            save_tracked_messages(TRACKED_REACTION_MESSAGES)
        except discord.Forbidden:
            await reaction.message.channel.send(f"❌ I don't have permission to assign the **{role_name}** role!")
        except discord.HTTPException as e:
            await reaction.message.channel.send(f"❌ Discord API error: {e}")
        except Exception as e:
            await reaction.message.channel.send(f"❌ Unexpected error: {e}")

    @bot.event
    async def on_reaction_remove(reaction, user):
        if user.bot:
            return

        message_id = reaction.message.id
        if message_id not in TRACKED_REACTION_MESSAGES:
            return

        tracked_data = TRACKED_REACTION_MESSAGES[message_id]
        emoji_str = str(reaction.emoji)

        possible_emoji_keys = [
            emoji_str,
            str(reaction.emoji),
            reaction.emoji.name if hasattr(reaction.emoji, 'name') else None,
            '👍',
            '\U0001f44d',
            '\ud83d\udc4d',
        ]

        emoji_key = None
        for possible_key in possible_emoji_keys:
            if possible_key and possible_key in tracked_data['emoji_map']:
                emoji_key = tracked_data['emoji_map'][possible_key]
                break

        if not emoji_key or emoji_key not in tracked_data['role_map']:
            return

        role_name = tracked_data['role_map'][emoji_key]
        guild = reaction.message.guild
        role = discord.utils.get(guild.roles, name=role_name)

        if role and role in user.roles:
            try:
                await user.remove_roles(role)
                await reaction.message.channel.send(f"✅ {user.mention} removed the **{role.name}** role!")
                save_tracked_messages(TRACKED_REACTION_MESSAGES)
            except discord.Forbidden:
                await reaction.message.channel.send(f"❌ I don't have permission to remove the **{role_name}** role!")
            except Exception as e:
                await reaction.message.channel.send(f"❌ Error removing role: {e}")
