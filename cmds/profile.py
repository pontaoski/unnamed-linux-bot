#!/usr/bin/env python3
import discord
import cmds.cmdutils
from cmds.cmdutils import default
import argparse
import pickledb

# 'dnf search query'
async def handle_message(message: discord.Message):
    db = pickledb.load('profile.db', True)
    query = cmds.cmdutils.get_content(message.content)
    query_array = query.split()
    args_dict = {}
    sender = message.author
    sender_id = sender.id

    if not query_array:
        await message.channel.send("Not enough arguments!")
        helpmsg = ""
        helpmsg += "```dsconfig\n"
        helpmsg += "# Syntax: sudo profile --flag value\n"
        helpmsg += " ( --user | -u )\n"
        helpmsg += " \tGet the user specified.\n"
        helpmsg += " ( --set-desktop-environment | -D )\n"
        helpmsg += " \tSet your desktop environment or window manager.\n"
        helpmsg += " ( --set-distro | -d )\n"
        helpmsg += " \tSet your distro.\n"
        helpmsg += " ( --set-shell | -s )\n"
        helpmsg += " \tSet your shell.\n"
        helpmsg += " ( --set-editor | -e )\n"
        helpmsg += " \tSet your editor.\n"
        helpmsg += " ( --set-languages | -p )\n"
        helpmsg += " \tSet your programming languages.\n"
        helpmsg += " ( --set-blurb | -b )\n"
        helpmsg += " \tSet your programming languages.\n"
        helpmsg += "```"
        await message.channel.send(helpmsg)

    while query_array:
        if query_array[0] == "-D" or query_array[0] == "--set-desktop-environment":
            query_array.pop(0)
            value = ""
            for index, argvalue in enumerate(query_array,start=0):
                if not "-" in argvalue:
                    value += "{} ".format(argvalue)
                else:
                    break

            if not query_array:
                continue
            args_dict["desktop"] = value.rstrip()
        if query_array[0] == "-d" or query_array[0] == "--set-distro":
            query_array.pop(0)
            value = ""
            for index, argvalue in enumerate(query_array,start=0):
                if not "-" in argvalue:
                    value += "{} ".format(argvalue)

            if not query_array:
                continue
            args_dict["distro"] = value.rstrip()
        if query_array[0] == "-s" or query_array[0] == "--set-shell":
            query_array.pop(0)
            value = ""
            for index, argvalue in enumerate(query_array,start=0):
                if not "-" in argvalue:
                    value += "{} ".format(argvalue)

            if not query_array:
                continue
            args_dict["shell"] = value.rstrip()
        if query_array[0] == "-e" or query_array[0] == "--set-editor":
            query_array.pop(0)
            value = ""
            for index, argvalue in enumerate(query_array,start=0):
                if not "-" in argvalue:
                    value += "{} ".format(argvalue)

            if not query_array:
                continue
            args_dict["editor"] = value.rstrip()
        if query_array[0] == "-p" or query_array[0] == "--set-languages":
            query_array.pop(0)
            value = ""
            for index, argvalue in enumerate(query_array,start=0):
                if not "-" in argvalue:
                    value += "{} ".format(argvalue)

            if not query_array:
                continue
            args_dict["langs"] = value.rstrip()
        if query_array[0] == "-b" or query_array[0] == "--set-blurb":
            query_array.pop(0)
            value = ""
            for index, argvalue in enumerate(query_array,start=0):
                if not "-" in argvalue:
                    value += "{} ".format(argvalue)

            if not query_array:
                continue
            args_dict["blurb"] = value.rstrip()
        if query_array[0] == "-u" or query_array[0] == "--user":
            query_array.pop(0)
            value = ""
            for index, argvalue in enumerate(query_array,start=0):
                if not "-" in argvalue:
                    value += "{} ".format(argvalue)

            if not query_array:
                continue
            args_dict["user"] = value.rstrip()
        
        query_array.pop(0)
            
    profile_updated = None
    if "desktop" in args_dict.keys():
        db.set(str(sender_id) + "_de", args_dict["desktop"])
        profile_updated = True
    if "distro" in args_dict.keys():
        db.set(str(sender_id) + "_distro", args_dict["distro"])
        profile_updated = True
    if "shell" in args_dict.keys():
        db.set(str(sender_id) + "_shell", args_dict["shell"])
        profile_updated = True
    if "editor" in args_dict.keys():
        db.set(str(sender_id) + "_editor", args_dict["editor"])
        profile_updated = True
    if "langs" in args_dict.keys():
        db.set(str(sender_id) + "_langs", args_dict["langs"])
        profile_updated = True
    if "blurb" in args_dict.keys():
        db.set(str(sender_id) + "_blurb", args_dict["blurb"])
        profile_updated = True

    if profile_updated is not None:
        await message.channel.send("Profile updated!")

    if "user" in args_dict.keys():
        mentioned_member = message.guild.get_member_named(args_dict["user"])
        try:
            mentioned_member = message.mentions[0]
        except IndexError:
            a="a"

        if mentioned_member is None:
            await message.channel.send("That person does not exist. Please be more specific, or check that they exist. If you were trying to use a command, please check your syntax.")
            return
        
        mmid = mentioned_member.id

        desktop = default(db.get(str(mentioned_member.id) + "_de"),"No DE/WM set.")
        distro  = default(db.get(str(mentioned_member.id) + "_distro"),"No distro set.")
        shell   = default(db.get(str(mentioned_member.id) + "_shell"),"No shell set.")
        editor  = default(db.get(str(mentioned_member.id) + "_editor"),"No editor set.")
        langs   = default(db.get(str(mentioned_member.id) + "_langs"),"No languages set.")
        blurb   = default(db.get(str(mentioned_member.id) + "_blurb"), None)

        pmsg = ""
        pmsg += "> **{}'s profile**\n".format(mentioned_member.display_name)
        pmsg += "> Distro: {}\n".format(distro)
        pmsg += "> DE/WM: {}\n".format(desktop)
        pmsg += "> Shell: {}\n".format(shell)
        pmsg += "> Editor: {}\n".format(editor)
        pmsg += "> Programming Languages: {}\n".format(langs)
        if blurb is not None:
            pmsg += "> \n"
            pmsg += "> *{}*\n".format(blurb)

        await message.channel.send(pmsg)