#!/usr/bin/env python3
import discord
import cmds.cmdutils
import urllib.parse
import requests

async def handle_message(message: discord.Message):
    await message.channel.trigger_typing()
    query = cmds.cmdutils.get_content(message.content)
    if len(query) == 0:
        await message.channel.send("Not enough args!")
    
    req = requests.get("https://archlinux.org/packages/search/json/?q={}&repo=Community&repo=Core&repo=Extra&repo=Multilib".format(urllib.parse.quote(query, safe='')))
    json = req.json()
    
    pkgs = []

    for pkg in json["results"]:
        pkgs.append(" ‣ `{}` - {}\n".format(pkg["pkgname"], pkg["pkgdesc"]))

    try:
        await message.channel.send("**{} search results for `{}` in Arch Linux**\n\n".format(len(pkgs), query))
        await message.channel.send("".join(pkgs[:3]))
    except:
        await message.channel.send("There was an error or your result did not return anything!")

async def handle_aur_message(message: discord.Message):
    await message.channel.trigger_typing()
    query = cmds.cmdutils.get_content(message.content)
    if len(query) == 0:
        await message.channel.send("Not enough args!")
    
    req = requests.get("https://aur.archlinux.org/rpc/?v=5&type=info&arg={}".format(urllib.parse.quote(query, safe='')))
    json = req.json()

    print(json)
    
    pkgs = []

    for pkg in json["results"]:
        pkgs.append(" ‣ `{}` - {}\n".format(pkg["Name"], pkg["Description"]))

    try:
        await message.channel.send("**{} search results for `{}` in the AUR**\n\n".format(len(pkgs), query))
        await message.channel.send("".join(pkgs[:3]))
    except:
        await message.channel.send("There was an error or your result did not return anything!")