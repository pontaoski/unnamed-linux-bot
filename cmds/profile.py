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

    helpmsg = ""
    helpmsg += "```dsconfig\n"
    helpmsg += "# Syntax: sudo profile --flag value\n"
    helpmsg += " ( --user | -u )\n"
    helpmsg += " \tGet the user specified.\n"
    helpmsg += " ( --set-desktop-environment | -w )\n"
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
    helpmsg += " \tSet your profile blurb.\n"
    helpmsg += "```"

    if not query_array:
        await message.channel.send("Not enough arguments!")
        await message.channel.send(helpmsg)
        return

    while query_array:
        distro_query = cmds.cmdutils.get_flag_value("-w", "--set-desktop-environment", query_array)
        if distro_query is not None:
            args_dict["desktop"] = distro_query
        distro_query = cmds.cmdutils.get_flag_value("-d", "--set-distro", query_array)
        if distro_query is not None:
            args_dict["distro"] = distro_query
        shell_query = cmds.cmdutils.get_flag_value("-s", "--set-shell", query_array)
        if shell_query is not None:
            args_dict["shell"] = shell_query
        editor_query = cmds.cmdutils.get_flag_value("-e", "--set-editor", query_array)
        if editor_query is not None:
            args_dict["editor"] = editor_query
        langs_query = cmds.cmdutils.get_flag_value("-p", "--set-languages", query_array)
        if langs_query is not None:
            args_dict["langs"] = langs_query
        blurb_query = cmds.cmdutils.get_flag_value("-b", "--set-blurb", query_array)
        if blurb_query is not None:
            args_dict["blurb"] = blurb_query
        user_query = cmds.cmdutils.get_flag_value("-u", "--user", query_array)
        if user_query is not None:
            args_dict["user"] = user_query
        
        query_array.pop(0)
            
    if args_dict == {}:
        await message.channel.send("Invalid arguments!")
        await message.channel.send(helpmsg)
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
        mentioned_member = cmds.cmdutils.get_user_closest_to_name(message.guild, args_dict["user"])
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