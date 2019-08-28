#!/usr/bin/env python3
import discord
import cmds.cmdutils
from cmds.cmdutils import _c

async def echo_message(message: discord.Message):
    lex = cmds.cmdutils.lex_command(message)
    cmd = _c(lex)
    await cmd.send_msg(content="{} said: ".format(message.author.display_name) + discord.utils.escape_mentions(cmd.content))
    return