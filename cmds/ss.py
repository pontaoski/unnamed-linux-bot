#!/usr/bin/env python3
import discord
import cmds.cmdutils
import pickledb

async def handle_message(message):
    db = pickledb.load('ss.db', True)

    query = cmds.cmdutils.get_content(message.content)
    query_array = query.split()

    sender = message.author
    sender_id = sender.id

    if not db.get(str(sender_id) + "_ss_url"):
        db.set(str(sender_id) + "_ss_url", "")
    if not db.get(str(sender_id) + "_ss_desc"):
        db.set(str(sender_id) + "_ss_desc", "")

    if query_array[0] == "set":
        query_array.pop(0)
        if not query_array:
            await message.channel.send("Invalid arguments!")
        
        if query_array[0] == "url":
            query_array.pop(0)
            if not query_array:
                await message.channel.send("Invalid arguments!")

            db.set(str(sender_id) + "_ss_url", query_array[0])

        elif query_array[0] == "desc":
            query_array.pop(0)
            if not query_array:
                await message.channel.send("Invalid arguments!")

            desc = " ".join(query_array)
            db.set(str(sender_id) + "_ss_desc", desc)

        else:
            await message.channel.send("Invalid arguments!")
    else:
        mentioned_member = message.guild.get_member_named(query)
        if mentioned_member is None:
            await message.channel.send("That person does not exist. Please be more specific, or check that they exist. If you were trying to use a command, please check your syntax.")
        url = db.get(str(mentioned_member.id) + "_ss_url")
        desc = db.get(str(mentioned_member.id) + "_ss_url")

        if desc is False:
            desc = ""

        if url is False:
            await message.channel.send(mentioned_member.display_name + " does not have a screenshot set!")

        embed = discord.Embed(title=mentioned_member.display_name + "'s screenshot", color=mentioned_member.colour, description=desc)
        embed.set_image(url=url)

        await message.channel.send(embed=embed)