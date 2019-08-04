#!/usr/bin/env python3
import discord
import cmds.cmdutils

async def handle_message(message: discord.Message):
    print("called")
    if "sudoer" in [y.name.lower() for y in message.author.roles] and not message.author.guild_permissions.administrator:
        print("not sudoer")
        return

    cmd = cmds.cmdutils.get_content(message.content)
    cmd_array = cmd.split()

    if cmd_array[0] == "stop":
        await message.channel.send("🛑 Stopping chat... 🛑")
        await message.channel.edit(slowmode_delay=30)
    elif cmd_array[0] == "start":
        await message.channel.send("✔️ Starting chat... ✔️")
        await message.channel.edit(slowmode_delay=0)
