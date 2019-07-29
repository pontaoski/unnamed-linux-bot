#!/usr/bin/env python3
import discord
import urllib.parse
import cmds.cmdutils
import requests
import json

# 'dnf search query'
async def handle_message(message):
    query = cmds.cmdutils.get_content(message.content)
    
    req = requests.get(f"https://apps.fedoraproject.org/packages/fcomm_connector" \
                       f"/xapian/query/search_packages/{{\"filters\":{{\"search\":" \
                       f"\"{query}\"}},\"rows_per_page\":10,\"start_row\":0}}")
    req_json = req.json()
    
    response = ""
    
    if (req_json["total_rows"] == 0):
        response += f"**No search results for \"{query}\" on Fedora Packages.**"
        
    else:
        response += f"**{req_json['total_rows']} search results for \"{query}\"" \
                    f" on Fedora Packages.**\n\n"
        
        add_count = 0
        for package in req_json['rows']:
            # only include top three results in response.
            if (add_count == 3): 
                break
            
            # only include in response if summary is not empty.
            if (package['summary'] != "no summary in mdapi"): 
                response += f"  ‣ `{package['name']}` - \"{package['summary']}\"\n"
                add_count += 1
                
            # prioritize adding sub-packages into results, if any, after the main package. 
            if ("sub_pkgs" in package.keys()):
                for sub_package in package['sub_pkgs']:
                    if (add_count == 3):
                        break
                    if (sub_package['summary'] != "no summary in mdapi"):
                        response += f"  ‣ `{sub_package['name']}` - \"{sub_package['summary']}\"\n"
                        add_count += 1
            
        if (add_count == 0):
            response += "  No packages with descriptions found in the first 10 results;\n"
        
        urlquery = urllib.parse.quote(query)
        response += f"\nView full results: <https://apps.fedoraproject.org/packages/s/{urlquery}>"

    # embed = discord.Embed(title="dnf search results for " + query, color=0x294172, url="https://apps.fedoraproject.org/packages/s/" + urlquery)
    await message.channel.send(response)
