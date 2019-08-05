#!/usr/bin/env python3
import discord
import cmds.cmdutils
from ast import literal_eval

async def handle_message(message: discord.Message):
    content = cmds.cmdutils.get_content(message.content)
    dict = literal_eval(content)
    embed = discord.Embed.from_dict(dict)
    await message.channel.send(embed=embed)
    await message.delete()
    return