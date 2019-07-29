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

dnf_obj = dnf.Base()

async def handle_message(message: discord.Message):
    global dnf_obj

    query = cmds.cmdutils.get_content(message.content)

    dnf_query = dnf_obj.sack.query()
    available_packages = dnf_query.available()
    available_packages = available_packages.filter(name__substr=query,arch=["noarch","x86_64"])

    pkgs = []

    for pkg in available_packages:
        pkgs.append(" ‣ `{}` - {}\n".format(pkg.name, pkg.summary))

    try:
        await message.channel.send("**{} search results for `{}` in openSUSE**\n\n".format(len(pkgs), query))
        await message.channel.send("".join(pkgs[:3]))
    except:
        await message.channel.send("There was an error!")


def init_dnf(config: configparser.ConfigParser):
    global dnf_obj
    
    dnf_obj.conf.ignorearch = True
    dnf_obj.conf.logdir = tempfile.mkdtemp(suffix="dnflog")
    dnf_obj.conf.reposdir = config["Zypper"]["RepoPath"]
    dnf_obj.conf.keepcache = True
    dnf_obj.conf.cachedir = tempfile.mkdtemp()
    
    dnf_obj.read_all_repos()

    print(config["Zypper"]["RepoPath"])

    dnf_obj.fill_sack(load_system_repo=False)
