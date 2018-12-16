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


@sopel.module.commands('listgen')
def mainfunctionnobeguine(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    bot.say("Generating a list of commands...")

    dispmsg = []
    moduletypes = ['dict', 'module', 'nickname', 'rule']
    moduleindex = []
    for comtype in moduletypes:
        comtypedict = str(comtype + "_commands")
        moduleindex.append(bot.memory["botdict"]["tempvals"][comtypedict].keys())

    # for mtype, mindex in zip(moduletypes, moduleindex):
        # bot.msg("#spicebottest", mtype + "    " + str(len(mindex)))

    moduleindex = [["tap"], ["dbbtest"], [str(bot.nick) + " " + 'update'], []]
    indexcount = len(moduleindex)
    for mtype, mindex in zip(moduletypes, moduleindex):
        indexcount -= 1
        commandcount = len(mindex)

        if commandcount:
            dispmsg.append(["(" + str(commandcount) + ") " + mtype + " commands:"])

        for command in mindex:
            commandcount -= 1

            comstring = []
            dictcomref = str(mtype + "_commands")

            # command dictionary
            dict_from_file = copy.deepcopy(bot.memory["botdict"]["tempvals"][dictcomref][str(command)])
            if "aliasfor" not in dict_from_file.keys():

                # dotcommand
                if dictcomref in ['nickname_commands', 'rule_commands']:
                    comstring.append(command)
                else:
                    comstring.append("." + command)

                # description
                if dict_from_file["description"]:
                    comstring.append("Description:  " + str(dict_from_file["description"]))

                # author
                if dict_from_file["author"]:
                    comstring.append("Author:  " + str(dict_from_file["author"]))

                # contributors
                if dict_from_file["contributors"]:
                    comstring.append("Contributors:  " + str(spicemanip(bot, dict_from_file["contributors"], "andlist")))

                # filepath
                if dict_from_file["filepath"]:
                    filepath = dict_from_file["filepath"].split("/home/spicebot/.sopel/" + str(bot.nick))[-1]
                    comstring.append("Filepath:  " + str(filepath))

                # alternative commands
                if dict_from_file["validcoms"]:
                    del dict_from_file["validcoms"][0]
                    if len(dict_from_file["validcoms"]):
                        comstring.append("Valid Alternates: " + str(spicemanip(bot, dict_from_file["validcoms"], "orlist")))

                # Usage
                if dict_from_file["example"]:
                    comstring.append("Example Usage:  " + str(dict_from_file["example"]))

                # Reply
                if dict_from_file["exampleresponse"]:
                    comstring.append("Example Reply:  " + str(dict_from_file["exampleresponse"]))

                # and to final
                dispmsg.append(comstring)

        if indexcount:
            dispmsg.append(["     "])

    pasteformat = []
    for comstring in dispmsg:
        pasteformat.append(comstring[0])
        del comstring[0]
        for remstring in comstring:
            pasteformat.append("  *  " + remstring)
    url = create_list(bot, botcom, '\n\n'.join(pasteformat))
    osd(bot, botcom.channel_current, 'say', "I've posted a list of my commands at " + str(url))


def create_list(bot, botcom, msg):
    msg = 'Command listing for {}@{}\n\n'.format(bot.nick, botcom.server) + msg
    payload = {"content": msg}
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    try:
        result = requests.post('https://ptpb.pw/', json=payload, headers=headers)
    except requests.RequestException:
        osd(bot, botcom.channel_current, 'say', "Sorry! Something went wrong.")
        logger.exception("Error posting commands")
        return
    result = result.json()
    if 'url' not in result:
        osd(bot, botcom.channel_current, 'say', "Sorry! Something went wrong.")
        logger.error("Invalid result %s", result)
        return
    url = result['url'].replace("https", "http")
    return url
