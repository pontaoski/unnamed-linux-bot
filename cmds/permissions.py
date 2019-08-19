#!/usr/bin/env python3
import discord
import cmds.cmdutils
from ast import literal_eval

permdict = {}

def save_dict():
    global permdict
    f = open("roles.db", "w")
    f.write(str(permdict))
    f.close()

def load_dict():
    global permdict
    f = open("roles.db", "r")
    contents = f.read()
    reactdict = literal_eval(contents)

def set_node(member: discord.Member, node: str, value: bool):
    global permdict
    load_dict()
    permdict.setdefault(member.id, {})
    permdict[member.id].setdefault(node, False)
    permdict[member.id][node] = value
    save_dict()

def get_node(member: discord.Member, node: str):
    global permdict
    load_dict()
    if member.id not in permdict.keys():
        return False
    if node not in permdict[member.id].keys():
        return False
    return permdict[member.id][node]

async def handle_message(message: discord.Message):
    query = cmds.cmdutils.get_content(message.content)
    queryᐸlistᐳ = query.split()

    if queryᐸlistᐳ[0] == "set":
        member = cmds.cmdutils.get_user_closest_to_name(message.guild, queryᐸlistᐳ[1])
        set_node(member,queryᐸlistᐳ[2],bool(queryᐸlistᐳ[3]))
        await message.channel.send("Permission node {} set to {} for {}!".format(queryᐸlistᐳ[2],queryᐸlistᐳ[3],member.display_name))

    elif queryᐸlistᐳ[0] == "get":
        member = cmds.cmdutils.get_user_closest_to_name(message.guild, queryᐸlistᐳ[1]) 
        value = get_node(member,queryᐸlistᐳ[2])
        await message.channel.send("Permission node {} is set to {} for {}!".format(queryᐸlistᐳ[2], str(value), member.display_name))