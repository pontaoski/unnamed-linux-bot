#!/usr/bin/env python3
import discord

async def handle_message(message):
    msg = ""
    msg += "Hello, I'm the Unnamed Linux Bot! And yes, that's my name!\n"
    msg += "I like helping out wherever.\n\n"
    msg += "You can see me and my pals' source at <https://github.com/unnamed-linux-community>!\n"
    msg += "Maybe you'd like to contribute as well?"
    await message.channel.send(msg)