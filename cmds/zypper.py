#!/usr/bin/env python3
import discord
import urllib.parse
import cmds.cmdutils
from cmds.cmdutils import _c
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

    lex = cmds.cmdutils.lex_command(message)
    cmd = _c(lex)
    
    if cmd.query_length == 0:
        await cmd.st("Not enough args!")

    dnf_query = dnf_obj.sack.query()
    available_packages = dnf_query.available()
    available_packages = available_packages.filter(name__substr=cmd.content,arch=["noarch","x86_64"])

    pkgs = []

    for pkg in available_packages:
        pkgs.append(" ‣ `{}` - {}\n".format(pkg.name, pkg.summary))

    try:
        await cmd.st("**{} search results for `{}` in openSUSE**\n\n".format(len(pkgs), cmd.content) + "".join(pkgs[:3]))
    except:
        await cmd.st("There was an error!")


def init_dnf(config: configparser.ConfigParser):
    global dnf_obj
    
    dnf_obj.conf.ignorearch = True
    dnf_obj.conf.logdir = config["Zypper"]["CachePath"]
    dnf_obj.conf.reposdir = config["Zypper"]["RepoPath"]
    dnf_obj.conf.keepcache = True
    dnf_obj.conf.cachedir = config["Zypper"]["CachePath"]
    
    dnf_obj.read_all_repos()

    print(config["Zypper"]["RepoPath"])

    dnf_obj.fill_sack(load_system_repo=False)
