#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module


# imports for system and OS access, directories
import os
import sys

# imports based on THIS file
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

comdict = {
            "author": "deathbybandaid",
            "contributors": [],
            "description": "",
            'privs': [],
            "example": "",
            "exampleresponse": "",
            }


"""
Based on
https://github.com/sdushantha/sherlock
"""


@sopel.module.commands('username', 'sherlock')
def mainfunction(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    if not botcom.multiruns:
        execute_main(bot, trigger, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    if "sherlock" not in bot.memory:
        sherlock_configs(bot)
    data = bot.memory['sherlock']
    netlist = []
    for social_network in data:
        netlist.append(str(social_network))

    username = spicemanip(bot, botcom.triggerargsarray, 1) or botcom.instigator
    botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, "2+", 'list')

    checklist = netlist
    checklistname = 'all'
    if bot_check_inlist(bot, username, netlist):
        checklistname = nick_actual(bot, username, netlist)
        checklist = [checklistname]
        username = spicemanip(bot, botcom.triggerargsarray, 1) or botcom.instigator

    osd(bot, botcom.channel_current, 'say', "Checking username " + username + " in " + checklistname + " network.")

    inlist = []
    notinlist = []

    for social_network in checklist:

        url = data.get(social_network).get("url").format(username)
        error_type = data.get(social_network).get("errorType")
        cant_have_period = data.get(social_network).get("noPeriod")

        if ("." in username) and (cant_have_period == "True"):
            while ("." in username):
                username = username.replace(".", '')

        r, error_type = make_request(url=url, error_type=error_type, social_network=social_network)

        if error_type == "message":
            error = data.get(social_network).get("errorMsg")
            # Checks if the error message is in the HTML
            if error not in r.text:
                inlist.append(social_network)
            else:
                notinlist.append(social_network)

        elif error_type == "status_code":
            # Checks if the status code of the repsonse is 404
            if not r.status_code == 404:
                inlist.append(social_network)
            else:
                notinlist.append(social_network)

        elif error_type == "response_url":
            error = data.get(social_network).get("errorUrl")
            # Checks if the redirect url is the same as the one defined in data.json
            if error not in r.url:
                inlist.append(social_network)
            else:
                notinlist.append(social_network)

    if inlist != []:
        osd(bot, botcom.channel_current, 'say', ["The username " + username + " is in the following:", spicemanip(bot, inlist, "andlist")])
    if notinlist != []:
        osd(bot, botcom.channel_current, 'say', ["The username " + username + " is NOT in the following:", spicemanip(bot, notinlist, "andlist")])


def sherlock_configs(bot):

    bot.memory['sherlock'] = dict()

    dirdict = {
                "name": "sherlock",
                "dirname": "Sherlock_Usernames",
                }

    filedicts, filecount = configs_dir_read(bot, dirdict)

    for dict_from_file in filedicts:

        comconf = dict_from_file["filename"]

        if comconf not in bot.memory['sherlock'].keys():
            bot.memory['sherlock'][comconf] = dict_from_file


def make_request(url, error_type, social_network):
    try:
        r = requests.get(url, headers=header)
        if r.status_code:
            return r, error_type
    except Exception as e:
        return None, ""
