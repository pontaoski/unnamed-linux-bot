#!/usr/bin/env python3
import discord
import urllib.parse
import cmds.cmdutils
import requests
import configparser

import dnf
import dnf.base
import dnf.conf
import dnf.const

mageia_dnf_obj = dnf.Base()

# 'dnf search query'
async def handle_message(message: discord.Message):
    global mageia_dnf_obj

    query = cmds.cmdutils.get_content(message.content)
    if len(query) == 0:
        await message.channel.send("Not enough args!")

    dnf_query = mageia_dnf_obj.sack.query()
    available_packages = dnf_query.available()
    available_packages = available_packages.filter(name__substr=query,arch=["noarch","x86_64"])

    pkgs = []

    for pkg in available_packages:
        pkgs.append(" ‣ `{}` - {}\n".format(pkg.name, pkg.summary))

    try:
        await message.channel.send("**{} search results for `{}` in Mageia**\n\n".format(len(pkgs), query))
        await message.channel.send("".join(pkgs[:3]))
    except:
        await message.channel.send("There was an error!")

def init_dnf(config: configparser.ConfigParser):
    global mageia_dnf_obj
    
    mageia_dnf_obj.conf.ignorearch = True
    mageia_dnf_obj.conf.logdir = config["Mageia"]["LogPath"]
    mageia_dnf_obj.conf.reposdir = config["Mageia"]["RepoPath"]
    mageia_dnf_obj.conf.keepcache = True
    mageia_dnf_obj.conf.cachedir = config["Mageia"]["CachePath"]
    
    mageia_dnf_obj.read_all_repos()

    print(config["Mageia"]["RepoPath"])

    mageia_dnf_obj.fill_sack(load_system_repo=False)