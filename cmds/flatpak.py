#!/usr/bin/env python3
import discord
import urllib.parse
import cmds.cmdutils

async def handle_message(message):
    query = cmds.cmdutils.get_content(message.content)
    urlquery = urllib.parse.quote(query)

#   embed = discord.Embed(title="flathub search results for " + query, color=0x4a86cf, url="https://flathub.org/apps/search/" + urlquery)
    await message.channel.send("flathub search results for " + query + ":\n" + "https://flathub.org/apps/search/" + urlquery)
