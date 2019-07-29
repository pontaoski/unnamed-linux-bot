#!/usr/bin/env python3
import discord
import cmds.cmdutils

async def handle_message(message):
    embed = discord.Embed(title="Welcome!", description="To verify that you are not a bot, please click the yellow heart.", color=0xdbc374)
    await message.channel.send(embed=embed)
    await message.delete()