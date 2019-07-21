#!/usr/bin/env python3
import discord
import cmds.cmdutils
import pickledb
import requests

async def handle_message(message):
    db = pickledb.load('ss.db', True)

    query = cmds.cmdutils.get_content(message.content)
    query_array = query.split()

    sender = message.author
    sender_id = sender.id

    screenshots = db.get("screenshots")
    if screenshots is False:
        db.set("screenshots", " ")
        screenshots = db.get("screenshots")
    
    screenshots_array = screenshots.split(',')

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
            if str(sender_id) not in screenshots:
                screenshots_array.append(str(sender_id))
                screenshots = ",".join(screenshots_array)
                db.set("screenshots", screenshots)
            await message.channel.send("Screenshot set!")


        elif query_array[0] == "desc":
            query_array.pop(0)
            if not query_array:
                await message.channel.send("Invalid arguments!")

            desc = " ".join(query_array)
            db.set(str(sender_id) + "_ss_desc", desc)
            await message.channel.send("Description set!")

        else:
            await message.channel.send("Invalid arguments!")

    elif query_array[0] == "ls" or query_array[0] == "list":
        await message.channel.trigger_typing()
        posttitle = "Screenshots in Unnamed Linux Community"
        postbody = ""

        for i in screenshots_array:
            ss_url = db.get(i + "_ss_url")
            desc = db.get(i + "_ss_desc")

            if desc is False:
                desc = ""

            if ss_url is False or ss_url == "":
                continue

            member = message.guild.get_member(int(i))
            
            if member is None:
                continue

            postbody += "\n# **" + member.display_name + "**\n"
            if desc != "":
                postbody += desc + "\n\n"
            else:
                postbody += "\n"

            postbody += "<img src=\"{url}\">".format(url=ss_url)

        postdict = {"body": postbody, "title": posttitle}
        r = requests.post("https://write.as/api/posts",json=postdict)
        r_json = r.json()
        post_id = r_json["data"]["id"]
        await message.channel.send("List of screenshots: https://write.as/" + post_id + ".md")

    else:
        mentioned_member = message.guild.get_member_named(query)
        try:
            mentioned_member = message.mentions[0]
        except IndexError:
            a="a"

        if mentioned_member is None:
            await message.channel.send("That person does not exist. Please be more specific, or check that they exist. If you were trying to use a command, please check your syntax.")
            return

        url = db.get(str(mentioned_member.id) + "_ss_url")
        desc = db.get(str(mentioned_member.id) + "_ss_desc")

        if desc is False:
            desc = ""

        if url is False or url == "":
            await message.channel.send(mentioned_member.display_name + " does not have a screenshot set!")
            return

        embed = discord.Embed(title=mentioned_member.display_name + "'s screenshot", color=mentioned_member.colour, description=desc)
        embed.set_image(url=url)

        await message.channel.send(embed=embed)