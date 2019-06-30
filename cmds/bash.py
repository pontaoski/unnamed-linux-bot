#!/usr/bin/env python3
import urllib.parse
import requests
import cmds.cmdutils

async def handle_message(message):
    cmd = cmds.cmdutils.get_content(message.content)
    
    if len(cmd) == 0:
        message.channel.send("Not enough args!")

    urlcmd = urllib.parse.quote(cmd)

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

    await message.channel.send("```\n" + message.author.display_name + "@unnamed-linux" + " > " + cmd + "\n" + output + "\n```")
