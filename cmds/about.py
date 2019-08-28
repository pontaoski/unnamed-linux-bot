#!/usr/bin/env python3
import discord
import cmds.cmdutils
from cmds.cmdutils import _c

async def handle_message(message):
    lex = cmds.cmdutils.lex_command(message)
    cmd = _c(lex)
    msg = ""
    msg += "Hello, I'm Cafétera!\n"
    msg += "I like helping out wherever.\n\n"
    msg += "You can see me and my pals' source at <https://github.com/linux-cafe>!\n"
    msg += "Maybe you'd like to contribute as well?"
    await cmd.st(content=msg)

async def handle_help_message(message):
    lex = cmds.cmdutils.lex_command(message)
    cmd = _c(lex)
    msg = ""
    msg += "Hello, I'm Cafétera!\n"
    msg += "Do you want to know how to use me?\n\n"
    msg += "Learn how at <https://linux-cafe.github.io/commands.html>!\n"
    await cmd.st(content=msg)