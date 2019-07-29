#!/usr/bin/env python3
import discord
import urllib.parse
import cmds.cmdutils
import requests
import configparser
import tempfile

import dnf
import dnf.base
import dnf.conf
import dnf.const

fedora_dnf_obj = dnf.Base()

# 'dnf search query'
async def handle_message(message: discord.Message):
    global fedora_dnf_obj

    query = cmds.cmdutils.get_content(message.content)

    dnf_query = fedora_dnf_obj.sack.query()
    available_packages = dnf_query.available()
    available_packages = available_packages.filter(name__substr=query,arch=["noarch","x86_64"])

    pkgs = []

    for pkg in available_packages:
        pkgs.append(" ‣ `{}` - {}\n".format(pkg.name, pkg.summary))

    try:
        await message.channel.send("**{} search results for `{}` in Fedora**\n\n".format(len(pkgs), query))
        await message.channel.send("".join(pkgs[:3]))
    except:
        await message.channel.send("There was an error!")

def init_dnf(config: configparser.ConfigParser):
    global fedora_dnf_obj
    
    fedora_dnf_obj.conf.ignorearch = True
    fedora_dnf_obj.conf.logdir = tempfile.mkdtemp(suffix="dnflog")
    fedora_dnf_obj.conf.reposdir = config["Dnf"]["RepoPath"]
    fedora_dnf_obj.conf.keepcache = True
    fedora_dnf_obj.conf.cachedir = tempfile.mkdtemp()
    
    fedora_dnf_obj.read_all_repos()

    print(config["Dnf"]["RepoPath"])

    fedora_dnf_obj.fill_sack(load_system_repo=False)