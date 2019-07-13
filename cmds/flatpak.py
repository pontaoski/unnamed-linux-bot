#!/usr/bin/env python3
import discord
import urllib.parse
import cmds.cmdutils
import json
import requests
import time

from os import path
from os import mkdir

# flatpak search 
async def handle_message(message):
    query = cmds.cmdutils.get_content(message.content)
    query_casefold = query.casefold()
    
    update_required = True
    force_update = False
    
    if "-r" in query_casefold.split(" "):
        force_update = True
        query_casefold = query_casefold.replace("-r", "").strip()
        query = query.replace("-r", "").strip()
    
    app_list = []
    
    if path.exists("cache"):
        if (path.exists("cache/flatpak.json") and force_update != True):
            with open("cache/flatpak.json") as flatpak_cache:
                app_list = json.load(flatpak_cache)
                
                # do not update if the cache is less than one hour old
                if app_list[-1]["timestamp"] - time.time() < 3600: 
                    update_required = False;
    else:
        mkdir("cache")
        
    if update_required:
        req = requests.get("https://flathub.org/api/v1/apps")
        app_list = json.loads(req.text)
        
        # adds the timestamp of the current database update to the end of the array. 
        timestamp_json = json.loads("{}")
        timestamp_json["timestamp"] = time.time()
        app_list.append(timestamp_json)
        
        flatpak_cache = open("cache/flatpak.json", mode="w")
        flatpak_cache.write(json.dumps(app_list))
        flatpak_cache.close()
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
        
        if query_casefold in app["name"].casefold():
            name_match.append(app)
            total_matches += 1
            continue
        
        if query_casefold in app["flatpakAppId"].casefold():
            appid_match.append(app)
            total_matches += 1
            continue
        
        if query_casefold in app["summary"].casefold():
            summary_match.append(app)
            total_matches += 1
            continue
        
    response = ""
        
    if total_matches == 0:
        response += '**No search results for "' + query + '" on Flathub.**'
    else:
        response += '**Search results for "' + query + '" on Flathub.**\n\n'
        
        for app in name_match:
            response += '  ‣ `' + app["name"] + '` - ' + app["summary"] + '\n'
        for app in appid_match:
            response += '  ‣ `' + app["name"] + '` - ' + app["summary"] + '\n'
        for app in summary_match:
            response += '  ‣ `' + app["name"] + '` - ' + app["summary"] + '\n'
        
        urlquery = urllib.parse.quote(query)
        response += '\nView full results: ' + '<https://flathub.org/apps/search/' + urlquery + '>'
        
    await message.channel.send(response)

    # embed = discord.Embed(title="flathub search results for " + query, color=0x4a86cf, url="https://flathub.org/apps/search/" + urlquery)
    # await message.channel.send("flathub search results for " + query + ":\n" + "https://flathub.org/apps/search/" + urlquery)
