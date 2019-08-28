#!/usr/bin/env python3
import discord
import urllib.parse
import cmds.cmdutils
from cmds.cmdutils import _c
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

    lex = cmds.cmdutils.lex_command(message)
    cmd = _c(lex)
    
    if cmd.query_length == 0:
        await cmd.st("Not enough args!")

    dnf_query = mageia_dnf_obj.sack.query()
    available_packages = dnf_query.available()
    available_packages = available_packages.filter(name__substr=cmd.content,arch=["noarch","x86_64"])

    pkgs = []

    for pkg in available_packages:
        pkgs.append(" ‣ `{}` - {}\n".format(pkg.name, pkg.summary))

    try:
        await cmd.st("**{} search results for `{}` in Mageia**\n\n".format(len(pkgs), cmd.content) + "".join(pkgs[:3]))
    except:
        await cmd.st("There was an error!")

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