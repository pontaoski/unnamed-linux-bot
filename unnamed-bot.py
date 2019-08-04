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
import cmds.info
import cmds.ss
import cmds.about
import cmds.welcomemsg
import cmds.zypper
import cmds.bz
import cmds.mageia
import cmds.chat

config = configparser.ConfigParser()

class UnnamedClient(discord.Client):

    # async def on_member_join(self, member):
        # channel = self.get_channel(int(config['Discord']['WelcomeChannel']))
        # message = await channel.send("Welcome to the server, <@" + str(member.id) + ">! \nPlease read our rules at https://linux-cafe.github.io/rules.html.\nWhen you have read them, click the heart that's the same color as the website's top bar.")
        # await message.add_reaction("💚")
        # await message.add_reaction("❤")
        # await message.add_reaction("💛")
        # await message.add_reaction("💙")

    async def on_raw_reaction_add(self, raw):
        channel = self.get_channel(int(config['Discord']['WelcomeChannel']))
        reaction_channel = self.get_channel(raw.channel_id)
        guild = self.get_guild(raw.guild_id)
        user = guild.get_member(raw.user_id)
        if (channel == reaction_channel):
            if(raw.emoji.name == "💛"):
                await user.add_roles(channel.guild.get_role(int(config['Discord']['WelcomeUserRole'])))

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        global config
        if message.author == self.user:
            logfile = open(config['Discord']['MsgLogPath'] + "/" + str(message.channel.id) + ".log", "a+")
            logfile.write("{} ({}) at {}\n".format(message.author.display_name, str(message.author.id), message.created_at.strftime("%Y-%m-%d %H:%M:%S")))
            logfile.write(message.clean_content + "\n")
            for i in message.embeds:
                logfile.write(str(i.to_dict()) + "\n\n")
            return

        elif message.content.startswith("sudo reload"):
            if message.author.guild_permissions.administrator:
                await self.change_presence(status=discord.Status.dnd)
                await message.channel.send("Reloading...")
                cmds.bash = reload(cmds.bash)
                cmds.dnf = reload(cmds.dnf)
                cmds.flatpak = reload(cmds.flatpak)
                cmds.autoslowmode = reload(cmds.autoslowmode)
                cmds.info = reload(cmds.info)
                cmds.ss = reload(cmds.ss)
                cmds.about = reload(cmds.about)
                cmds.welcomemsg = reload(cmds.welcomemsg)
                cmds.zypper = reload(cmds.zypper)
                cmds.bz = reload(cmds.bz)
                cmds.mageia = reload(cmds.mageia)
                cmds.chat = reload(cmds.chat)
                try:
                    print("Initializing dnf...")
                    cmds.dnf.init_dnf(config)
                except:
                    print("Dnf error!")
                try:
                    print("Initializing zypper...")
                    cmds.zypper.init_dnf(config)
                except:
                    print("Zypper error!")
                try:
                    print("Initializing mageia...")
                    cmds.mageia.init_dnf(config)
                except:
                    print("Mageia error!")
                await message.channel.send("Reloaded!")
                await self.change_presence(status=discord.Status.online)

        elif message.content.startswith("sudo eval "):
            if message.author.guild_permissions.administrator:
                cmd = message.content[10:]
                exec(cmd)

        elif message.content.startswith("flatpak search"):
            await cmds.flatpak.handle_message(message)

        elif message.content.startswith(("dnf search ", "dnf se ")):
            await message.channel.trigger_typing()
            await cmds.dnf.handle_message(message)

        elif message.content.startswith(("dnf mageia-search ", "dnf mse ")):
            await message.channel.trigger_typing()
            await cmds.mageia.handle_message(message)

        elif message.content.startswith(("zypper search ", "zypper se ", "zyp se ", "zyp search ")):
            await message.channel.trigger_typing()
            await cmds.zypper.handle_message(message)

        elif message.content.startswith("bash -c "):
            await message.channel.trigger_typing()
            await cmds.bash.handle_message(message)

        elif message.content.startswith("sudo info "):
            await cmds.info.handle_message(message)
        elif message.content.startswith("sudo info"):
            await message.channel.send("Not enough arguments!\nUsage: `sudo info <query>`")

        elif message.content.startswith("sudo about"):
            await cmds.about.handle_message(message)

        elif message.content.startswith("sudo ss "):
            await cmds.ss.handle_message(message)
        elif message.content.startswith("sudo ss"):
            await message.channel.send("Not enough arguments!\nSee `sudo help` for how to use this command.")

        elif message.content.startswith("sudo chat "):
            await cmds.chat.handle_message(message)
        
        elif message.content.startswith("sudo help"):
            await message.channel.send("See help at https://linux-cafe.github.io/.")
        
        elif message.content.startswith("sudo welcomemessage"):
            await cmds.welcomemsg.handle_message(message)

        await cmds.autoslowmode.handle_message(message)
        await cmds.bz.handle_message(message)
        logfile = open(config['Discord']['MsgLogPath'] + "/" + str(message.channel.id) + ".log", "a+")
        logfile.write("{} ({}) at {}\n".format(message.author.display_name, str(message.author.id), message.created_at.strftime("%Y-%m-%d %H:%M:%S")))
        for i in message.embeds:
            logfile.write(str(i.to_dict()) + "\n\n")
        logfile.write(message.clean_content + "\n\n")

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
    
try:
    print("Initializing dnf...")
    cmds.dnf.init_dnf(config)
except:
    print("Dnf error!")
try:
    print("Initializing zypper...")
    cmds.zypper.init_dnf(config)
except:
    print("Zypper error!")
try:
    print("Initializing mageia...")
    cmds.mageia.init_dnf(config)
except:
    print("Mageia error!")

client = UnnamedClient()
client.run(config['Discord']['Token'])
