#!/usr/bin/env python3
import urllib.parse
import requests
import cmds.cmdutils
from cmds.cmdutils import _c

async def handle_message(message):
    lex = cmds.cmdutils.lex_command(message)
    cmd = _c(lex)

    if cmd.query_length == 0:
        await message.channel.send("Not enough args!")

    urlcmd = urllib.parse.quote(cmd.content)

    URL = "https://rextester.com/rundotnet/api?LanguageChoice=38&Program=" + urlcmd

    r = requests.get(url = URL)
    data = r.json()
    output = ""
    
    if data["Warnings"] is not None:
        output += data["Warnings"]

    if data["Errors"] is not None:
        output += data["Errors"]

    if data["Result"] is not None:
        output += data["Result"]

    await cmd.st(content="```\n" + message.author.display_name + "@unnamed-linux" + " > " + cmd.content + "\n" + output + "\n```")
