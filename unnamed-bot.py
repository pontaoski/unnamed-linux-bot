#!/usr/bin/env python3
from importlib import reload
from os import path

import discord
from discord.utils import get
import configparser

import cmds
import cmds.bash
import cmds.dnf
import cmds.flatpak
import cmds.autoslowmode

class UnnamedClient(discord.Client):

    async def on_member_join(self, member):
        channel = self.get_channel(int(config['Discord']['WelcomeChannel']))
        message = await channel.send("Welcome to the server, <@" + str(member.id) + ">! To join, please react to the heart emoji.")
        await message.add_reaction("😶")
        await message.add_reaction("💬")
        await message.add_reaction("💛")
        await message.add_reaction("👰")

    async def on_reaction_add(self, reaction, user):
        channel = self.get_channel(int(config['Discord']['WelcomeChannel']))
        if (reaction.message.channel == channel):
            if(reaction.emoji == "💛"):
                await user.add_roles(channel.guild.get_role(int(config['Discord']['WelcomeUserRole'])))

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
                cmds.flatpak = reload(cmds.flatpak)
                cmds.autoslowmode = reload(cmds.autoslowmode)

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

        await cmds.autoslowmode.handle_message(message)

config = configparser.ConfigParser()

if path.exists("config.ini"):
    config.read("config.ini")
else:
    config['Discord'] = {}
    config['Discord']['Token'] = "token-here"
    config['Discord']['WelcomeChannel'] = "id-here"
    config['Discord']['WelcomeUsersRole'] = "id-here"
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("You have not configured this bot. Please use config.ini to configure this bot.")
    exit()
    
client = UnnamedClient()
client.run(config['Discord']['Token'])
