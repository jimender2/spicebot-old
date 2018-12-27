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
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


"""
This Cycles through all of the dictionary commands
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_dict_coms(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "bot_info", "txt_files"]):
        pass

    dict_command_configs(bot)

    bot_startup_requirements_set(bot, "dict_coms")


# Command configs
def dict_command_configs(bot):

    dirdict = {
                "name": "dict_commands",
                "dirname": "Dictionary_replies",
                "configname": "dictcoms",
                }

    filedicts, filecount = configs_dir_read(bot, dirdict)
    bot.memory['dict_commands'] = dict()
    bot.memory['dict_commands_count'] = filecount

    for dict_from_file in filedicts:

        comconf = dict_from_file["filename"]

        # default command to filename
        if "validcoms" not in dict_from_file.keys():
            dict_from_file["validcoms"] = [comconf]
        elif dict_from_file["validcoms"] == []:
            dict_from_file["validcoms"] = [comconf]
        elif not isinstance(dict_from_file['validcoms'], list):
            dict_from_file["validcoms"] = [dict_from_file["validcoms"]]

        maincom = dict_from_file["validcoms"][0]
        if len(dict_from_file["validcoms"]) > 1:
            comaliases = spicemanip(bot, dict_from_file["validcoms"], '2+', 'list')
        else:
            comaliases = []

        # check for tuple dict keys and split
        for validkey in dict_from_file.keys():
            if isinstance(validkey, tuple):
                tuple_bak = validkey
                tuple_contents_bak = dict_from_file[validkey]
                del dict_from_file[validkey]
                for var in tuple_bak:
                    dict_from_file[var] = tuple_contents_bak

        if maincom not in bot.memory['dict_commands'].keys():

            # check that type is set, use cases will inherit this if not set
            if "type" not in dict_from_file.keys():
                foldername = dict_from_file["filepath"].split("/" + dict_from_file["filename"])[0]
                foldername = str(foldername).split("/")[-1]
                dict_from_file["type"] = foldername
            if dict_from_file["type"] not in valid_com_types:
                dict_from_file["type"] = 'simple'

            # Don't process these.
            keysprocessed = []
            keysprocessed.extend(["validcoms", "filepath"])

            # the command must have an author
            if "author" not in dict_from_file.keys():
                dict_from_file["author"] = "deathbybandaid"
            keysprocessed.append("author")

            # the command must have a contributors list
            if "contributors" not in dict_from_file.keys():
                dict_from_file["contributors"] = []
            if not isinstance(dict_from_file["contributors"], list):
                dict_from_file["contributors"] = [dict_from_file["contributors"]]
            if "deathbybandaid" not in dict_from_file["contributors"]:
                dict_from_file["contributors"].append("deathbybandaid")
            if dict_from_file["author"] not in dict_from_file["contributors"]:
                dict_from_file["contributors"].append(dict_from_file["author"])
            keysprocessed.append("contributors")

            if "hardcoded_channel_block" not in dict_from_file.keys():
                dict_from_file["hardcoded_channel_block"] = []
            keysprocessed.append("hardcoded_channel_block")

            if "example" not in dict_from_file.keys():
                dict_from_file["example"] = str("." + maincom)

            if "exampleresponse" not in dict_from_file.keys():
                dict_from_file["exampleresponse"] = None

            if "description" not in dict_from_file.keys():
                dict_from_file["description"] = None

            if "privs" not in dict_from_file.keys():
                dict_from_file["privs"] = []

            keysprocessed.extend(["validcoms", "filepath", "description", "exampleresponse", "example", "privs"])

            # handle basic required dict handling
            dict_required = ["?default"]
            dict_from_file = bot_dict_use_cases(bot, maincom, dict_from_file, dict_required)
            keysprocessed.extend(dict_required)

            # remove later
            keysprocessed.append("type")

            # all other keys not processed above are considered potential use cases
            otherkeys = []
            for otherkey in dict_from_file.keys():
                if otherkey not in keysprocessed:
                    otherkeys.append(otherkey)
            if otherkeys != []:
                dict_from_file = bot_dict_use_cases(bot, maincom, dict_from_file, otherkeys)
            keysprocessed.extend(otherkeys)

            bot.memory['dict_commands'][maincom] = dict_from_file
            for comalias in comaliases:
                if comalias not in bot.memory['dict_commands'].keys():
                    bot.memory['dict_commands'][comalias] = {"aliasfor": maincom}


# goes with the above function, is used for iteration over use cases
def bot_dict_use_cases(bot, maincom, dict_from_file, process_list):

    for mustbe in process_list:

        # All of the above need to be in the dict if not
        if mustbe not in dict_from_file.keys():
            dict_from_file[mustbe] = dict()

        # verify if already there, that the key is a dict
        if not isinstance(dict_from_file[mustbe], dict):
            dict_from_file[mustbe] = dict()

        # Each usecase for the command must have a type, flat files inherit this type
        if "type" not in dict_from_file[mustbe].keys():
            if "type" in dict_from_file.keys():
                dict_from_file[mustbe]["type"] = dict_from_file["type"]
            else:
                dict_from_file[mustbe]["type"] = "simple"

        # each usecase needs to know if it can be updated. Default is false
        if "updates_enabled" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["updates_enabled"] = False
        if dict_from_file[mustbe]["updates_enabled"]:
            if dict_from_file[mustbe]["updates_enabled"] not in ["shared", "user"]:
                dict_from_file[mustbe]["updates_enabled"] = "shared"

        # each usecase needs to know if it needs a target
        if "target_required" not in dict_from_file[mustbe].keys():
            if dict_from_file[mustbe]["type"] in ['target', 'targetplusreason']:
                dict_from_file[mustbe]["target_required"] = True
            else:
                dict_from_file[mustbe]["target_required"] = False
        if "target_backup" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["target_backup"] = False
        if "target_bypass" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["target_bypass"] = []

        # special target reactions
        for reason in ['self', 'bot', 'bots', 'offline', 'unknown', 'privmsg', 'diffchannel', 'diffbot']:
            if 'react_'+reason not in dict_from_file[mustbe].keys():
                dict_from_file[mustbe]['react_'+reason] = False

        # each usecase needs to know if it needs input for fillintheblank
        if "blank_required" not in dict_from_file[mustbe].keys():
            if dict_from_file[mustbe]["type"] in ['fillintheblank', 'targetplusreason', "translate"]:
                dict_from_file[mustbe]["blank_required"] = True
            else:
                dict_from_file[mustbe]["blank_required"] = False
        if "blank_backup" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["blank_backup"] = False
        if "blank_fail" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["blank_fail"] = ["This command requires input."]
        if not isinstance(dict_from_file[mustbe]["blank_fail"], list):
            dict_from_file[mustbe]["blank_fail"] = [dict_from_file[mustbe]["blank_fail"]]

        if "blank_phrasehandle" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["blank_phrasehandle"] = False
        if dict_from_file[mustbe]["blank_phrasehandle"]:
            if not isinstance(dict_from_file[mustbe]["blank_phrasehandle"], list):
                dict_from_file[mustbe]["blank_phrasehandle"] = [dict_from_file[mustbe]["blank_phrasehandle"]]

        if "response_fail" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["response_fail"] = False
        if dict_from_file[mustbe]["response_fail"]:
            if not isinstance(dict_from_file[mustbe]["response_fail"], list):
                dict_from_file[mustbe]["response_fail"] = [dict_from_file[mustbe]["response_fail"]]

        if dict_from_file[mustbe]["updates_enabled"]:
            adjust_nick_array(bot, str(bot.nick), 'long', 'sayings', maincom + "_" + str(mustbe), dict_from_file[mustbe]["responses"], 'startup')
            dict_from_file[mustbe]["responses"] = get_nick_value(bot, str(bot.nick), 'long', 'sayings', maincom + "_" + str(mustbe)) or []

        # each usecase needs a response
        if "responses" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["responses"] = []

        # verify responses are in list form
        if not isinstance(dict_from_file[mustbe]["responses"], list):
            if dict_from_file[mustbe]["responses"] in bot.memory["botdict"]["tempvals"]['txt_files'].keys():
                dict_from_file[mustbe]["responses"] = bot.memory["botdict"]["tempvals"]['txt_files'][dict_from_file[mustbe]["responses"]]
            elif str(dict_from_file[mustbe]["responses"]).startswith(tuple(["https://", "http://"])):
                page = requests.get(dict_from_file[mustbe]["responses"], headers=header)
                tree = html.fromstring(page.content)
                if page.status_code == 200:
                    htmlfile = urllib.urlopen(dict_from_file[mustbe]["responses"])
                    lines = htmlfile.read().splitlines()
                    dict_from_file[mustbe]["responses"] = lines
            else:
                dict_from_file[mustbe]["responses"] = [dict_from_file[mustbe]["responses"]]

        # each usecase needs a prefixtext
        if "prefixtext" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["prefixtext"] = False
        if dict_from_file[mustbe]["prefixtext"]:
            if not isinstance(dict_from_file[mustbe]["prefixtext"], list):
                dict_from_file[mustbe]["prefixtext"] = [dict_from_file[mustbe]["prefixtext"]]

        # each usecase needs a suffixtext
        if "suffixtext" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["suffixtext"] = False
        if dict_from_file[mustbe]["suffixtext"]:
            if not isinstance(dict_from_file[mustbe]["suffixtext"], list):
                dict_from_file[mustbe]["suffixtext"] = [dict_from_file[mustbe]["suffixtext"]]

        # Translations
        if "translations" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["translations"] = False
        if dict_from_file[mustbe]["translations"]:
            if not isinstance(dict_from_file[mustbe]["translations"], list):
                dict_from_file[mustbe]["translations"] = [dict_from_file[mustbe]["translations"]]

        # make sure we have the smaller variation list
        if "replyvariation" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["replyvariation"] = []
        if not isinstance(dict_from_file[mustbe]["replyvariation"], list):
            dict_from_file[mustbe]["replyvariation"] = [dict_from_file[mustbe]["replyvariation"]]

        # This is to provide functionality for flat dictionaries responses
        if dict_from_file[mustbe]["responses"] == [] and mustbe == "?default":
            if "responses" in dict_from_file.keys():
                if isinstance(dict_from_file["responses"], list):
                    dict_from_file[mustbe]["responses"].extend(dict_from_file["responses"])
                else:
                    dict_from_file[mustbe]["responses"].append(dict_from_file["responses"])
                del dict_from_file["responses"]

        # Verify responses list is not empty
        if dict_from_file[mustbe]["responses"] == []:
            dict_from_file[mustbe]["responses"].append("No " + str(mustbe) + " responses set for " + str(maincom) + ".")

        # Some commands run query mode
        if "search_fail" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["search_fail"] = None
        if dict_from_file[mustbe]["search_fail"]:
            if not isinstance(dict_from_file[mustbe]["search_fail"], list):
                dict_from_file[mustbe]["search_fail"] = [dict_from_file[mustbe]["search_fail"]]

        if "selection_allowed" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["selection_allowed"] = True

        # Translations
        if "randnum" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["randnum"] = False
        if dict_from_file[mustbe]["randnum"]:
            if not isinstance(dict_from_file[mustbe]["randnum"], list):
                dict_from_file[mustbe]["randnum"] = [0, 50]
            if len(dict_from_file[mustbe]["randnum"]) == 1:
                dict_from_file[mustbe]["randnum"] = [0, dict_from_file[mustbe]["randnum"][0]]

        if "hardcoded_channel_block" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["hardcoded_channel_block"] = []

        if "privs" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["privs"] = []

    return dict_from_file
