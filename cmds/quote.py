#!/usr/bin/env python3
import discord
import cmds.cmdutils
from cmds.cmdutils import _c

async def handle_message(message: discord.Message):
    cmd = _c(cmds.cmdutils.lex_command(message))
    
    helpmsg = ""
    helpmsg += "```dsconfig\n"
    helpmsg += "# Syntax: sudo quote --message id --channel id\n"
    helpmsg += " ( --message | -m )\n"
    helpmsg += " \tThe message ID to quote. Required.\n"
    helpmsg += " ( --channel | -c )\n"
    helpmsg += " \tThe channel ID of the message. Required.\n"
    helpmsg += " ( --reply | -r )\n"
    helpmsg += " \tReply to the message you're quoting.\n"
    helpmsg += "```"

    query_array = cmd.query_array

    if not query_array:
        await cmd.st("You didn't pass any arguments!\n\n" + helpmsg)
        return

    mid = None
    cid = None

    if cmd.get_flag_pair("-m", "--message") is not None:
        mid = cmd.get_flag_pair("-m", "--message")

    if cmd.get_flag_pair("-c", "--channel") is not None:
        cid = cmd.get_flag_pair("-c", "--channel")

    if mid is None or cid is None:
        await cmd.st("Not enough arguments!\n\n" + helpmsg)
        return

    guild = message.guild
    channel = guild.get_channel(int(cid))
    quoted_msg = await channel.fetch_message(int(mid))

    reply = None

    if cmd.get_flag_pair("-r", "--reply") is not None:
        reply = cmd.get_flag_pair("-r", "--reply")

    msg_to_send = """
**{}** said:
{}
""".format(quoted_msg.author.display_name, quoted_msg.clean_content)
    if reply is not None:
        msg_to_send += "\n**{}** replied:\n{}".format(message.author.display_name, reply)

    await cmd.st(msg_to_send)