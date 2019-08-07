#!/usr/bin/env python3
import discord
from discord.utils import get
import cmds.cmdutils
import pickledb
from ast import literal_eval

reactdict = {}

async def handle_reaction(client: discord.Client, reaction: discord.RawReactionActionEvent):
    global reactdict
    load_dict()
    guild = client.get_guild(reaction.guild_id)
    channel = client.get_channel(reaction.channel_id)
    message = await channel.fetch_message(reaction.message_id)
    member = guild.get_member(reaction.user_id)
    if not str(reaction.message_id) in reactdict.keys():
        return
    emoji = reaction.emoji
    emoji_id = emoji.id if emoji.is_custom_emoji() else str(emoji)
    messagedict = reactdict[str(reaction.message_id)]
    if not str(emoji_id) in messagedict.keys():
        return
    role = get(guild.roles, id=int(messagedict[str(emoji_id)]))
    if role in member.roles:
        await member.remove_roles(role)
    else:
        await member.add_roles(role)
    save_dict()
    return

async def handle_message(message: discord.Message):
    global reactdict
    load_dict()
    query = cmds.cmdutils.get_content(message.content)
    query_array = query.split()
    if query_array[0] == "addrole":
        query_array.pop(0)
        if not query_array:
            await message.channel.send("Invalid arguments!")
        reactdict.setdefault(query_array[0], {})
        reactdict[query_array[0]][query_array[1]] = query_array [2]

    save_dict()
    return

def save_dict():
    global reactdict
    f = open("roles.db", "w")
    f.write(str(reactdict))
    f.close()

def load_dict():
    global reactdict
    f = open("roles.db", "r")
    contents = f.read()
    reactdict = literal_eval(contents)

