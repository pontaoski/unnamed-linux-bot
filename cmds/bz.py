#!/usr/bin/env python3
import discord
import urllib.parse
import cmds.cmdutils
import requests
import bugzilla
import libxml2
import base64
from libpagure import Pagure
import gitlab
from github import Github
from phabricator import Phabricator

def split_bz(str):
    return str.split("#")

async def phabricator_message(tag, message: discord.Message):
    tags = split_bz(tag)
    phab = Phabricator()
    revision = phab.api.differential.getrevision(revision_id=int(tags[1]))
    author = phab.api.user.query(phids=[revision.authorPHID])[0]

    summary = ""

    summary += "<https://phabricator.kde.org/D{}>\n".format(tags[1])
    summary += "> **{}** ({}) - D{}\n".format(author["realName"], author["userName"], tags[1])
    summary += "> Status - {}\n".format(revision.statusName)
    summary += "> \n"
    summary += "> {}".format(revision.title)

    await message.channel.send(summary)

async def github_message(tag, message: discord.Message):
    tags = split_bz(tag)
    g = Github()
    repo = g.get_repo(tags[1])
    issue = repo.get_issue(number=int(tags[2]))
    summary = ""

    summary += "<{}>\n".format(issue.html_url)
    summary += "> **{}** - Issue **{}** at **{}**\n".format(issue.user.login, tags[2], tags[1])
    summary += "> Status - {}\n".format(issue.state)
    summary += "> \n"
    summary += "> {}".format(issue.title)

    await message.channel.send(summary)

async def gitlab_message(tag, message: discord.Message):
    tags = split_bz(tag)
    instance_url = "https://" + tags[1]
    gl = gitlab.Gitlab(instance_url)
    project = gl.projects.get(tags[2], lazy=True)
    summary = ""
    for i in project.issues.list():
        if i.iid == int(tags[3]):
            summary += "<{}>\n".format(i.web_url)
            summary += "> **{}** ({}) - Issue **{}** at **{}**\n".format(i.author["name"], i.author["username"], i.iid, tags[2])
            summary += "> Status - {}\n".format(i.state)
            summary += "> \n"
            summary += "> {}".format(i.title)
            await message.channel.send(summary)
    
async def pagure_message(tag, message):
    tags = split_bz(tag)
    instance_url = "https://" + tags[1]
    pg = Pagure(instance_url=instance_url,pagure_repository=tags[2])
    issue = pg.issue_info(tags[3])
    
    summary = ""

    summary += "> **{}** ({}) - Issue **{}** at **{}**\n".format(issue["user"]["fullname"], issue["user"]["name"], tags[3], tags[2])
    summary += "> Status - **{}**\n".format(issue["status"])
    summary += "> \n"
    summary += "> {}".format(issue["title"])

    await message.channel.send("{}/{}/issue/{}".format(instance_url, tags[2], tags[3]))
    await message.channel.send(summary)

async def bugzilla_message(api, tag, message, generic=False):
    bzapi = None
    if not generic:
        bzapi = bugzilla.Bugzilla(api)
        split_str = split_bz(tag)
        id = split_str[1]
    else:
        split_str = split_bz(tag)
        bzapi = bugzilla.Bugzilla(split_str[1])
        id = split_str[2]

    bug = bzapi.getbug(int(id))
    summary = ""

    bug_author_realname = None
    try:
        bug_author_realname = bug.creator_detail["real_name"]
    except:
        bug_author_realname = None

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

    if "bz#" in message.content:
        for i in words:
            if "bz#" in i:
                await bugzilla_message("generic", i, message, generic=True)

    if "pgr#" in message.content:
        for i in words:
            if "pgr#" in i:
                await pagure_message(i, message)
    
    if "gl#" in message.content:
        for i in words:
            if "gl#" in i:
                await gitlab_message(i, message)
        
    if "gh#" in message.content:
        for i in words:
            if "gh#" in i:
                await github_message(i, message)

    if "phabd#" in message.content:
        for i in words:
            if "phabd#" in i:
                await phabricator_message(i, message)

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