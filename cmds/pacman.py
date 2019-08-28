#!/usr/bin/env python3
import discord
import cmds.cmdutils
from cmds.cmdutils import _c
import urllib.parse
import requests

async def handle_message(message: discord.Message):
    await message.channel.trigger_typing()
    
    lex = cmds.cmdutils.lex_command(message)
    cmd = _c(lex)

    if cmd.query_length == 0:
        await message.channel.send("Not enough args!")
    
    req = requests.get("https://archlinux.org/packages/search/json/?q={}&repo=Community&repo=Core&repo=Extra&repo=Multilib".format(urllib.parse.quote(cmd.content, safe='')))
    json = req.json()
    
    pkgs = []

    for pkg in json["results"]:
        pkgs.append(" ‣ `{}` - {}\n".format(pkg["pkgname"], pkg["pkgdesc"]))

    try:
        await cmd.st("**{} search results for `{}` in Arch Linux**\n\n".format(len(pkgs), cmd.content) + "".join(pkgs[:3]))
    except:
        await cmd.st("There was an error or your result did not return anything!")

async def handle_aur_message(message: discord.Message):
    await message.channel.trigger_typing()
    
    lex = cmds.cmdutils.lex_command(message)
    cmd = _c(lex)

    if cmd.query_length == 0:
        await cmd.st("Not enough args!")
    
    req = requests.get("https://aur.archlinux.org/rpc/?v=5&type=info&arg={}".format(urllib.parse.quote(cmd.content, safe='')))
    json = req.json()

    print(json)
    
    pkgs = []

    for pkg in json["results"]:
        pkgs.append(" ‣ `{}` - {}\n".format(pkg["Name"], pkg["Description"]))

    try:
        await cmd.st("**{} search results for `{}` in the AUR**\n\n".format(len(pkgs), query) + "".join(pkgs[:3]))
    except:
        await cmd.st("There was an error or your result did not return anything!")