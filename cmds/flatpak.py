#!/usr/bin/env python3
import discord
import urllib.parse
import cmds.cmdutils
from cmds.cmdutils import _c
import json
import requests
import time

from pathlib import Path

# flatpak search 
async def handle_message(message):
    lex = cmds.cmdutils.lex_command(message)
    cmd = _c(lex)

    if cmd.query_length == 0:
        await cmd.st("Not enough args!")
    query_casefold = query.casefold()
    
    update_required = True
    force_update = False
    
    if "-r" in query_casefold.split(" "):
        force_update = True
        query_casefold = query_casefold.replace("-r", "").strip()
        query = query.replace("-r", "").strip()
    
    app_list = []
    cache_dir = Path("./cache")
    cache_file = cache_dir / "flatpak.json"
    
    if (cache_dir).is_dir():
        if (cache_file.is_file() and force_update != True):
            with cache_file.open() as flatpak_cache:
                app_list = json.load(flatpak_cache)
                
                # do not update if the cache is less than one hour old
                if app_list[-1]['timestamp'] - time.time() < 3600: 
                    update_required = False;
    else:
        Path.mkdir(cache_dir)
        
    if update_required:
        req = requests.get("https://flathub.org/api/v1/apps")
        app_list = json.loads(req.text)
        
        # adds the timestamp of the current database update to the end of the array. 
        timestamp_json = json.loads(f"{{\"timestamp\" : {time.time()}}}")
        app_list.append(timestamp_json)
        
        cache_file.write_text(json.dumps(app_list))
        print("flatpak cache updated in cache/flatpak.json")
        
    name_match = []
    appid_match = []
    summary_match = []
    total_matches = 0
    
    for app in app_list:
        # stops at 3 matches 
        if total_matches == 3:
            break
        
        # I would want to print total number of matches possible, but this 
        # feels like a waste of calculation because it might mismatch with 
        # what it appears on the site (the search algorithm might be 
        # different). And it doesn't really affect the usage of the bot, so
        # maybe we'll just leave it like that for now. 
        
        # do not attempt to search in the timestamp row
        if "timestamp" in app.keys():
            continue
        
        if query_casefold in app['name'].casefold():
            name_match.append(app)
            total_matches += 1
            continue
        
        if query_casefold in app['flatpakAppId'].casefold():
            appid_match.append(app)
            total_matches += 1
            continue
        
        if query_casefold in app['summary'].casefold():
            summary_match.append(app)
            total_matches += 1
            continue
        
    response = ""
        
    if total_matches == 0:
        response += f"**No search results for \"{query}\" on Flathub.**"
    else:
        response += f"**Search results for \"{query}\" on Flathub.**\n\n"
        
        for app in name_match:
            response += f"  ‣ `{app['name']}` - {app['summary']}\n"
        for app in appid_match:
            response += f"  ‣ `{app['name']}` - {app['summary']}\n"
        for app in summary_match:
            response += f"  ‣ `{app['name']}` - {app['summary']}\n"
        
        urlquery = urllib.parse.quote(query)
        response += f"\nView full results: <https://flathub.org/apps/search/{urlquery}>"
        
    await cmd.st(response)

    # embed = discord.Embed(title="flathub search results for " + query, color=0x4a86cf, url="https://flathub.org/apps/search/" + urlquery)
    # await message.channel.send("flathub search results for " + query + ":\n" + "https://flathub.org/apps/search/" + urlquery)
