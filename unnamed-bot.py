#!/usr/bin/env python3
from importlib import reload
import os.path
from os import path

import discord
import configparser

import cmds
import cmds.bash
import cmds.dnf
import cmds.flatpak

class UnnamedClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        elif message.content.startswith("sudo reload"):
            if message.author.guild_permissions.administrator:
                await message.channel.send("Reloaded!")
                cmds.bash = reload(cmds.bash)
                cmds.dnf = reload(cmds.dnf)

        elif message.content.startswith("sudo eval "):
            if message.author.guild_permissions.administrator:
                cmd = message.content[10:]
                exec(cmd)

        elif message.content.startswith("flatpak search"):
            await cmds.flatpak.handle_message(message)

        elif message.content.startswith(("dnf search ", "dnf se ")):
            await cmds.dnf.handle_message(message)

        elif message.content.startswith("bash -c "):
            await message.channel.trigger_typing()
            await cmds.bash.handle_message(message)

config = configparser.ConfigParser()

if path.exists("config.ini"):
    config.read("config.ini")
else:
    config['Discord'] = {}
    config['Discord']['Token'] = "token-here"
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("You have not configured this bot. Please use config.ini to configure this bot.")
    exit()
    
client = UnnamedClient()
client.run(config['Discord']['Token'])