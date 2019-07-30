#!/usr/bin/env python3
import discord
import urllib.parse
import cmds.cmdutils
import requests
import bugzilla
import libxml2
import base64

def split_bz(str):
    return str.split("#")

async def bugzilla_message(api, tag, message):
    split_str = split_bz(tag)
    id = split_str[1]

    bzapi = bugzilla.Bugzilla(api)
    bug = bzapi.getbug(int(id))
    summary = ""

    bug_author_realname = bug.creator_detail["real_name"]
    bug_author = bug.creator
    if bug_author_realname is not None:
        bug_author = "**{}** ({})".format(bug_author_realname, bug_author)
    bug_summary = bug.summary
    bug_status = bug.status
    bug_severity = bug.severity
    bug_priority = bug.priority
    bug_version = bug.version
    bug_product = bug.product
    bug_component = bug.component

    await message.channel.send(bug.weburl)
    summary += "> {} - Bug {}\n".format(bug_author, id)
    summary += "> *Status - {}* | *Product - {}* | *Component - {}*\n".format(bug_status,bug_product,bug_component)
    summary += "> *Severity - {}* | *Priority - {}* | *Version - {}*\n".format(bug_severity, bug_priority, bug_version)
    summary += "> \n"
    summary += "> {}".format(bug_summary)
    await message.channel.send(summary)

    print(bug.__dict__)

async def handle_message(message: discord.Message):
    words = message.content.split()
    if "boo#" in message.content:
        for i in words:
            if "boo#" in i:
                await bugzilla_message("bugzilla.opensuse.org", i, message)
    
    if "rhbz#" in message.content:
        for i in words:
            if "rhbz#" in i:
                await bugzilla_message("bugzilla.redhat.com", i, message)

    if "mgabz#" in message.content or "mga#" in message.content:
        for i in words:
            if "mgabz#" in i or "mga#" in i:
                await bugzilla_message("bugs.mageia.org", i, message)

    if "kdebz#" in message.content:
        for i in words:
            if "kdebz#" in i:
                await bugzilla_message("bugs.kde.org", i, message)

    if "bsc#" in message.content:
        for i in words:
            if "bsc#" in i:
                await bugzilla_message("bugzilla.suse.com", i, message)

    if "obssr#" in message.content:
        for i in words:
            if "obssr#" in i:
                split_str = split_bz(i)
                id = split_str[1]
                auth_creds = ('zyp_user', 'zyp_pw_1')
                r = requests.get('https://api.opensuse.org/request/' + id, auth=auth_creds)
                doc = libxml2.parseDoc(r.text)
                context = doc.xpathNewContext()
                res = context.xpathEval("/request/description")
                description = res[0].getContent()
                res = context.xpathEval("/request/state/@name")
                state = res[0].getContent()
                res = context.xpathEval("/request/action/@type")
                action = res[0].getContent()
                res = context.xpathEval("/request/action/source/@project")
                source = res[0].getContent()
                res = context.xpathEval("/request/action/source/@package")
                source_pkg = res[0].getContent()
                res = context.xpathEval("/request/action/target/@project")
                target = res[0].getContent()
                res = context.xpathEval("/request/action/target/@package")
                target_pkg = res[0].getContent()
                await message.channel.send("https://build.opensuse.org/request/show/{}".format(id))
                summary =  "> **SR#{}** - {} - **{}**\n".format(id,description,state)
                summary += "> {} - [{}:{} -> {}:{}]".format(action, source, source_pkg, target, target_pkg)
                await message.channel.send(summary)