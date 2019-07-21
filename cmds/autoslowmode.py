#!/usr/bin/env python3
import cmds.cmdutils
import threading
import discord

slowdict = {}
async def disable_slowmode(message):
    print("disable called")
    await message.channel.edit(slowmode_delay=0)

async def handle_message(message):
    global slowdict
    author = str(message.author.id)
    time = message.created_at
    if (message.author.bot):
        return

    if slowdict.get(author+"-lasttime", None) is not None:
        if slowdict.get(author+"-messagecount", None) is not None:
            if (time - slowdict[author+"-lasttime"]).total_seconds() > 6:
                slowdict[author+"-lasttime"] = time
                slowdict[author+"-messagecount"] = 1
            else:
                slowdict[author+"-messagecount"] += 1
                if slowdict[author+"-messagecount"] >= 5:
                    print("trigger slowmode")
                    embed = discord.Embed(color=0xFFFFFF, title="Looks like someone's spamming!")
                    embed.set_image(url="https://pics.me.me/you-do-not-spark-joy-goodbye-goodbye-42709155.png")
                    await message.channel.send(embed=embed)
        else:
            slowdict[author+"-messagecount"] = 1
    else:
        slowdict[author+"-lasttime"] = time
        slowdict[author+"-messagecount"] = 1

    # await message.channel.send(str((time - slowdict[author+"-lasttime"]).total_seconds()) + " " + str(slowdict[author+"-messagecount"]))
