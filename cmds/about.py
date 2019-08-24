#!/usr/bin/env python3
import discord

async def handle_message(message):
    msg = ""
    msg += "Hello, I'm Cafétera!\n"
    msg += "I like helping out wherever.\n\n"
    msg += "You can see me and my pals' source at <https://github.com/linux-cafe>!\n"
    msg += "Maybe you'd like to contribute as well?"
    await message.channel.send(msg)

async def handle_help_message(message):
    msg = ""
    msg += "Hello, I'm Cafétera!\n"
    msg += "Do you want to know how to use me?\n\n"
    msg += "Learn how at <https://linux-cafe.github.io/commands.html>!\n"
    await message.channel.send(msg)