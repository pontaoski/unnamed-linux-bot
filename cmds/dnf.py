#!/usr/bin/env python3
import discord
import urllib.parse
import cmds.cmdutils

# 'dnf search query'
async def handle_message(message):
    query = cmds.cmdutils.get_content(message.content)
    urlquery = urllib.parse.quote(query)

#   embed = discord.Embed(title="dnf search results for " + query, color=0x294172, url="https://apps.fedoraproject.org/packages/s/" + urlquery)
    await message.channel.send("dnf search results for " + query + ":\n" + "https://apps.fedoraproject.org/packages/s/" + urlquery)