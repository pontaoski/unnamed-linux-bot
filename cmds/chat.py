#!/usr/bin/env python3
import discord
import cmds.cmdutils
from cmds.cmdutils import _c

async def handle_message(message: discord.Message):
    if "sudoer" in [y.name.lower() for y in message.author.roles] and not message.author.guild_permissions.administrator:
        return

    lex = cmds.cmdutils.lex_command(message)
    cmd = _c(lex)

    if cmd.query_array[0] == "stop":
        await cmd.st("🛑 Stopping chat... 🛑")
        await message.channel.edit(slowmode_delay=30)
    elif cmd.query_array[0] == "start":
        await cmd.st("✔️ Starting chat... ✔️")
        await message.channel.edit(slowmode_delay=0)
