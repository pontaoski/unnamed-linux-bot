#!/usr/bin/env python3
import discord
import cmds.cmdutils
import urllib.parse
import requests
import json

# 'dnf search query'
async def handle_message(message):
    query = cmds.cmdutils.get_content(message.content)
    urlquery = urllib.parse.quote(query)
    await message.channel.trigger_typing()

    wikirequest = None
    wikijson = None

    try:
        wikirequest = requests.get("https://wikipedia.org/w/api.php?action=opensearch&search=" + urlquery + "&format=json&suggest=1&redirects=resolve")
        wikijson = wikirequest.json()
    except:
        await message.channel.send("Whoops! Looks like there was an error using Wikipedia's API.")

    msgToSend = ""
    if "may refer to" in wikijson[2][0]:
        msgToSend += "**" + wikijson[2][0] + "**" + "\n\n"
        if wikijson[2][1] is not None:
            msgToSend += wikijson[2][1] + "\n\n"
        if wikijson[2][2] is not None:
            msgToSend += wikijson[2][2] + "\n\n"
        if wikijson[2][3] is not None:
            msgToSend += wikijson[2][3] + "\n\n"
    else:
        msgToSend += "**" + wikijson[1][0] + "**" + "\n\n"
        msgToSend += wikijson[2][0] + "\n\n"
        msgToSend += "<" + wikijson[3][0] + ">"

    await message.channel.send(msgToSend)

