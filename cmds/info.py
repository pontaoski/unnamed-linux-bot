#!/usr/bin/env python3
import discord
import cmds.cmdutils
from cmds.cmdutils import _c
import urllib.parse
import requests
import json

# 'dnf search query'
async def handle_message(message):
    lex = cmds.cmdutils.lex_command(message)
    cmd = _c(lex)

    if cmd.query_length == 0:
        await cmd.st("Not enough args!")
    urlquery = urllib.parse.quote(cmd.content)
    await message.channel.trigger_typing()

    msgToSend = ""

    if "arch" in cmd.content.lower():
        msgToSend += "**Arch Linux**\n\n"
        msgToSend += "An independent rolling release distro. You can install it if you can read, but you’ll probably want some other skills before you try this one out.\n\n"
        msgToSend += "**Package Manager** - `pacman`\n"
        msgToSend += "**Package Format** - `pkg.tar.xz`\n"
        msgToSend += "**Community Repository** - AUR"
    elif "ubuntu" in cmd.content.lower():
        msgToSend += "**Ubuntu**\n\n"
        msgToSend += "Debian-based distribution backed by Canonical. Perfect for whatever you’re doing if it doesn’t require the latest software. Just avoid the snaps, alright?\n\n"
        msgToSend += "**Package Manager** - `apt`\n"
        msgToSend += "**Package Format** - `deb`\n"
        msgToSend += "Community Repository - https://www.ubuntuupdates.org/ppas"
    elif "fedora" in cmd.content.lower():
        msgToSend += "**Fedora**\n\n"
        msgToSend += "The Fedora Project is backed by Red Hat and is treated as the upstream source for the commercial Red Hat Enterprise Linux. Arguably the distro that does GNOME how the developers intended it best. Fedora, like Ubuntu, comes in flavours of different DEs. \nHas five variants: Workstation, Server, CoreOS, Silverblue and IoT.\nCoreOS is for Container Environments\nSilverblue is transactional desktop with an immutable core-image, rpm-ostree overlays and flatpaks\nIoT is for embedded devices.\n\n"
        msgToSend += "**Package Manager** - `dnf` or `rpm-ostree`\n"
        msgToSend += "**Package Format** - `rpm`"



    if not msgToSend == "":
        await cmd.st(msgToSend)
        return

    wikirequest = None
    wikijson = None

    try:
        wikirequest = requests.get("https://wikipedia.org/w/api.php?action=opensearch&search=" + urlquery + "&format=json&suggest=1&redirects=resolve")
        wikijson = wikirequest.json()
    except:
        await cmd.st("Whoops! Looks like there was an error using Wikipedia's API.")

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

    await cmd.st(msgToSend)

