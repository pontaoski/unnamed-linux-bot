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
import cmds.embed
import cmds.rolemenu
import cmds.profile
import cmds.permissions
import cmds.pacman

config = configparser.ConfigParser()
commands = {
    "sudo about":                                                           cmds.about.handle_message,
    "bash -c":                                                              cmds.bash.handle_message,
    "sudo chat":                                                            cmds.chat.handle_message,
    **dict.fromkeys(['dnf search', 'dnf se'],                               cmds.dnf.handle_message),
    **dict.fromkeys(['flatpak search', 'flatpak se'],                       cmds.flatpak.handle_message),
    "sudo info":                                                            cmds.info.handle_message,
    **dict.fromkeys(["dnf mageia-search", "dnf mse"],                       cmds.mageia.handle_message),
    "sudo profile":                                                         cmds.profile.handle_message,
    "rolemenu -c":                                                          cmds.rolemenu.handle_message,
    "sudo ss":                                                              cmds.ss.handle_message,
    "sudo welcomemessage":                                                  cmds.welcomemsg.handle_message,
    **dict.fromkeys(["zypper search", "zypper se", "zyp search", "zyp se"], cmds.zypper.handle_message),
    "sudo perm":                                                            cmds.permissions.handle_message,
    "sudo embed":                                                           cmds.embed.handle_message,
    "sudo help":                                                            cmds.about.handle_help_message,
    "pacman -Ss":                                                           cmds.pacman.handle_message,
    "yay -Ss":                                                              cmds.pacman.handle_aur_message
}

class UnnamedClient(discord.Client):
            
    async def handle_command_message(self, message: discord.Message):
        global commands
        command = ' '.join(message.content.split()[:2])
        func = commands.get(command, None)
        if command == "sudo reload":
            cmds.permissions = reload(cmds.permissions)

        if func is not None:
            await func(message)

    async def on_raw_reaction_add(self, raw):
        await cmds.rolemenu.handle_reaction(self, raw)
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

        await self.handle_command_message(message)

        await cmds.autoslowmode.handle_message(message)
        await cmds.bz.handle_message(message)
        logfile = open(config['Discord']['MsgLogPath'] + "/" + str(message.channel.id) + ".log", "a+")
        logfile.write("{} ({}) at {} - ID {}\n".format(message.author.display_name, str(message.author.id), message.created_at.strftime("%Y-%m-%d %H:%M:%S"), str(message.id)))
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
