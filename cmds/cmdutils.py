#!/usr/bin/env python
import discord
import asyncio
from fuzzywuzzy import process

lexes = {}

async def message_delete(message: discord.Message):
    lex = lex_command(message)
    lexes.remove(lex)
    await lex.delete()

async def clear_lexes(message: discord.Message):
    if "sudoer" in [y.name.lower() for y in message.author.roles] and not message.author.guild_permissions.administrator:
        return

    global lexes
    lexes = {}


class LexedCommand:
    content = ""
    flags = {}
    id = None
    message = None
    sent_message = None
    query_array = None
    query_length = None

    async def se(self, embed):
        await self.send_msg(embed=embed)
    async def st(self, content):
        await self.send_msg(content=content)

    async def delete(self):
        await self.message.delete()
        global lexes

    async def send_msg(self, content=None, embed=None):
        if self.sent_message is not None:
            await self.sent_message.edit(content=content, embed=embed) 
        else:
            self.sent_message = await self.message.channel.send(content, embed=embed)

    def get_flag_pair(self, short: str, lang: str):
        if short in self.flags.keys():
            return self.flags[short]
        elif lang in self.flags.keys():
            return self.flags[lang]
        else:
            return None

    def __lex_flags(self, content: str):
        array = content.split()[2:]
        for index, i in enumerate(array,start=0):
            if "--" == i:
                self.content = " ".join(array[index+1:])
                break
            if "-" in i:
                val = ""
                for ii in array[index+1:]:
                    if not "-" in ii:
                        val += "{} ".format(ii)
                    else:
                        break
                self.flags[i] = val.rstrip()
        if self.flags == {}:
            self.content = " ".join(array)
        return

    def __init_msg(self, msg: discord.Message):
        self.message = msg
        self.query_array = get_content(self.message.content).split()
        self.query_length = len(self.query_array)
        self.__lex_flags(self.message.content)

    def relex(self, new_msg: discord.Message):
        self.__init_msg(new_msg)

    def __init__(self, message: discord.Message):
        self.id = message.id
        self.__init_msg(message)

def lex_command(message):
    global lexes
    if message.id in lexes.keys():
        lexes[message.id].relex(message)
        return lexes[message.id].id
    cmd = LexedCommand(message)
    lexes[cmd.id] = cmd
    return cmd.id

def _c(id):
    return get_lexed_command(id)

def get_lexed_command(id):
    global lexes
    return lexes[id]
    

def get_content(string, trim_words=2):
    array = string.split()
    return " ".join(array[trim_words:])

def default(get, default):
    if get is False:
        return default
    elif get is None:
        return default
    else:
        return get

def get_user_closest_to_name(guild: discord.Guild, name: str):
    members = guild.members
    member_names = []
    for i in members:
        member_names.append(i.display_name)
    closest = process.extractOne(name, member_names)
    if closest is None:
        return None
    return guild.get_member_named(closest[0])

def get_flag_value(short: str, long: str, query_array):
    if query_array[0] == short or query_array[0] == long:
        query_array.pop(0)
        value = ""
        for index, argvalue in enumerate(query_array,start=0):
            if not "-" in argvalue:
                value += "{} ".format(argvalue)
            else:
                break
        return str(value.rstrip())
    else:
        return None