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
def bot_startup_feeds(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "bot_info", "txt_files"]):
        pass

    feed_configs(bot)

    bot_startup_requirements_set(bot, "feeds")


# Command configs
def feed_configs(bot):

    feedcount, feedopenfail = 0, 0
    filescan = []
    bot.memory["botdict"]["tempvals"]['feeds'] = dict()
    bot.memory["botdict"]["tempvals"]['feeds_loaded'] = []

    quick_coms_path = bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"] + "Modules/Feeds/" + str(bot.nick) + "/"
    if os.path.exists(quick_coms_path) and os.path.isdir(quick_coms_path):
        if not os.path.isfile(quick_coms_path) and len(os.listdir(quick_coms_path)) > 0:
            filescan.append(quick_coms_path)

    if "feeds" in bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration'].keys():
        if "extra" in bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration']["feeds"].keys():
            if "," not in str(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration']["feeds"]["extra"]):
                extradirs = [str(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration']["feeds"]["extra"])]
            else:
                extradirs = str(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration']["feeds"]["extra"]).split(",")
            for extra in extradirs:
                quick_coms_path_extra = bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"] + "Modules/Feeds/" + str(extra) + "/"
                if os.path.exists(quick_coms_path_extra) and os.path.isdir(quick_coms_path_extra):
                    if not os.path.isfile(quick_coms_path_extra) and len(os.listdir(quick_coms_path_extra)) > 0:
                        filescan.append(quick_coms_path_extra)

    # proceed with file iteration
    for directory in filescan:

        # iterate over organizational folder
        for comconf in os.listdir(directory):
            comconf_file_path = os.path.join(directory, comconf)

            if os.path.isfile(comconf_file_path):
                bot.msg("#spicebottest", str(comconf))

                # check if command file is already in the list
                if comconf not in bot.memory["botdict"]["tempvals"]['feeds_loaded']:
                    bot.memory["botdict"]["tempvals"]['feeds_loaded'].append(comconf)

                    # Read dictionary from file, if not, enable an empty dict
                    filereadgood = True
                    inf = codecs.open(comconf_file_path, "r", encoding='utf-8')
                    infread = inf.read()
                    try:
                        dict_from_file = eval(infread)
                    except Exception as e:
                        filereadgood = False
                        stderr("Error loading feed %s: %s (%s)" % (comconf, e, comconf_file_path))
                        dict_from_file = dict()
                    # Close File
                    inf.close()

                    bot.msg("#spicebottest", str(dict_from_file))

                    if filereadgood and isinstance(dict_from_file, dict):

                        feedcount += 1

                        if "feedtype" not in dict_from_file.keys():
                            dict_from_file["feedtype"] = "rss"

                        if "displayname" not in dict_from_file.keys():
                            dict_from_file["displayname"] = None

                        if "url" not in dict_from_file.keys():
                            dict_from_file["url"] = None

                        if dict_from_file["feedtype"] == "github":

                            if "lastbuildtype" not in dict_from_file.keys():
                                dict_from_file["lastbuildtype"] = "updated"

                            if "lastbuildparent" not in dict_from_file.keys():
                                dict_from_file["lastbuildparent"] = 1

                            if "lastbuildchild" not in dict_from_file.keys():
                                dict_from_file["lastbuildchild"] = 0

                            if "titletype" not in dict_from_file.keys():
                                dict_from_file["titletype"] = "title"

                            if "titleparent" not in dict_from_file.keys():
                                dict_from_file["titleparent"] = 1

                            if "titlechild" not in dict_from_file.keys():
                                dict_from_file["titlechild"] = 0

                            if "linktype" not in dict_from_file.keys():
                                dict_from_file["linktype"] = "link"

                            if "linkparent" not in dict_from_file.keys():
                                dict_from_file["linkparent"] = 2

                            if "linkchild" not in dict_from_file.keys():
                                dict_from_file["linkchild"] = "href"

                        if comconf not in bot.memory["botdict"]["tempvals"]['feeds'].keys():
                            bot.memory["botdict"]["tempvals"]['feeds'][comconf] = dict_from_file
                    else:
                        feedopenfail += 1
    if feedcount > 1:
        stderr('\n\nRegistered %d feed files,' % (feedcount))
        stderr('%d feed files failed to load\n\n' % feedopenfail)
    else:
        stderr("Warning: Couldn't load any feed files")

    bot.memory["botdict"]["tempvals"]['feed_count'] = feedcount


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

    return dict_from_file


def bot_dictcom_feeds(bot, botcom):

    dispmsg = bot_dictcom_feeds_handler(bot, botcom, True)
    if dispmsg == []:
        osd(bot, botcom.channel_current, 'say', botcom.maincom + " appears to have had an unknown error.")
    else:
        osd(bot, botcom.channel_current, 'say', dispmsg)


def bot_dictcom_feeds_handler(bot, botcom, displayifnotnew=True):

    dispmsg = []
    titleappend = False

    url = botcom.dotcommand_dict["url"]
    if not url:
        dispmsg.append("URL missing.")
        return dispmsg

    page = requests.get(url, headers=header)
    tree = html.fromstring(page.content)

    if page.status_code == 200:

        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=pytz.UTC)

        displayname = botcom.dotcommand_dict["displayname"]

        feed_type = botcom.dotcommand_dict["feedtype"]

        if feed_type in ['rss', 'youtube', 'github']:

            lastbuildcurrent = get_nick_value(bot, str(bot.nick), 'long', 'feeds', botcom.maincom + '_lastbuildcurrent') or datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
            lastbuildcurrent = parser.parse(str(lastbuildcurrent))

            xml = page.text
            xml = xml.encode('ascii', 'ignore').decode('ascii')
            xmldoc = minidom.parseString(xml)

            lastbuildtype = botcom.dotcommand_dict["lastbuildtype"]

            lastBuildXML = xmldoc.getElementsByTagName(lastbuildtype)

            lastbuildparent = int(botcom.dotcommand_dict["lastbuildparent"])

            lastbuildchild = int(botcom.dotcommand_dict["lastbuildchild"])

            lastBuildXML = lastBuildXML[lastbuildparent].childNodes[lastbuildchild].nodeValue
            lastBuildXML = parser.parse(str(lastBuildXML))

            if displayifnotnew or lastBuildXML > lastbuildcurrent:

                titleappend = True

                titletype = botcom.dotcommand_dict["titletype"]

                titles = xmldoc.getElementsByTagName(titletype)

                titleparent = botcom.dotcommand_dict["titleparent"]

                titlechild = int(botcom.dotcommand_dict["titlechild"])

                title = titles[titleparent].childNodes[titlechild].nodeValue

                if feed_type == 'github':
                    authors = xmldoc.getElementsByTagName('name')
                    author = authors[0].childNodes[0].nodeValue
                    dispmsg.append(author + " committed")

                title = unicode_string_cleanup(title)

                dispmsg.append(title)

                linktype = botcom.dotcommand_dict["linktype"]

                links = xmldoc.getElementsByTagName(linktype)

                linkparent = botcom.dotcommand_dict["linkparent"]

                linkchild = botcom.dotcommand_dict["linkchild"]

                if str(linkchild).isdigit():
                    linkchild = int(linkchild)
                    link = links[linkparent].childNodes[linkchild].nodeValue.split("?")[0]
                else:
                    link = links[linkparent].getAttribute(linkchild)
                dispmsg.append(link)

                if not displayifnotnew:
                    set_nick_value(bot, str(bot.nick), 'long', 'feeds', botcom.maincom + '_lastbuildcurrent', str(lastBuildXML))

    if titleappend and botcom.dotcommand_dict["displayname"]:
        dispmsg.insert(0, "[" + displayname + "]")

    return dispmsg
