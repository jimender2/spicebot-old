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
bot.nick do this
@rule('^\.(.*)')
@rule('(.*)')
"""


# TODO make sure restart and update save database
@rule('^\.(.*)')
@sopel.module.thread(True)
def mainfunctionnobeguine(bot, trigger):

    # command must start with
    if not str(trigger).startswith(tuple(['.'])):
        return

    botcom = botcom_symbol_trigger(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    execute_main(bot, trigger, botcom)
    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    # command issued, check if valid
    botcom.dotcommand = spicemanip(bot, botcom.triggerargsarray, 1).lower()[1:]
    if botcom.dotcommand in bot.memory["botdict"]["tempvals"]['dict_commands'].keys() and botcom.dotcommand not in bot.memory['botdict']['tempvals']['module_commands'].keys():
        bot_dictcom_handle(bot, botcom)


def bot_dictcom_handle(bot, botcom):

    # command aliases
    if "aliasfor" in bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand].keys():
        botcom.dotcommand = bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["aliasfor"]

    # simplify usage of the bot command going forward
    botcom.dotcommand_dict = copy.deepcopy(bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand])

    # remainder, if any is the new arg list
    botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+')

    # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
    if not botcom.dotcommand:
        return

    botcom.maincom = botcom.dotcommand_dict["validcoms"][0]

    # execute function based on command type
    botcom.commandtype = botcom.dotcommand_dict["type"].lower()

    # allow && splitting
    botcom.multiruns = True
    if not botcom.channel_priv:
        if botcom.maincom in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["multirun_disabled_commands"].keys():
            botcom.multiruns = False

    if not botcom.multiruns:
        bot_dictcom_process(bot, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')

            # bot_dictcom_simple(bot, botcom)  # TODO rename
            botcom.completestring = spicemanip(bot, botcom.triggerargsarray, 0)

            bot_dictcom_process(bot, botcom)


def bot_dictcom_process(bot, botcom):

    # use the default key, unless otherwise specified
    botcom.responsekey = "?default"

    # handling for special cases
    posscom = spicemanip(bot, botcom.triggerargsarray, 1)
    if posscom.lower() in [command.lower() for command in botcom.dotcommand_dict.keys()]:
        for command in botcom.dotcommand_dict.keys():
            if command.lower() == posscom.lower():
                posscom = command
        botcom.responsekey = posscom
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
    botcom.commandtype = botcom.dotcommand_dict[botcom.responsekey]["type"]

    botcom.nonstockoptions = []
    for command in botcom.dotcommand_dict.keys():
        if command not in ["?default", "validcoms", "contributors", "author", "type", "filepath", "hardcoded_channel_block", "description", "exampleresponse", "example", "privs"]:
            botcom.nonstockoptions.append(command)

    # This allows users to specify which reply by number by using an ! and a digit (first or last in string)
    validspecifides = ['block', 'unblock', 'last', 'random', 'count', 'view', 'add', 'del', 'remove', 'special', 'contribs', 'contrib', "contributors", 'author', "alias", "filepath", "enable", "disable", "multiruns", "description", "exampleresponse", "example", "usage", "privs"]
    botcom.specified = None
    argone = spicemanip(bot, botcom.triggerargsarray, 1)
    if str(argone).startswith("--") and len(str(argone)) > 2:
        if str(argone[2:]).isdigit():
            botcom.specified = int(argone[2:])
        elif bot_check_inlist(bot, str(argone[2:]), validspecifides):
            botcom.specified = str(argone[2:]).lower()
        elif bot_check_inlist(bot, str(argone[2:]), botcom.nonstockoptions):
            botcom.specified = str(argone[2:]).lower()
            botcom.responsekey = botcom.specified
        else:
            try:
                botcom.specified = w2n.word_to_num(str(argone[1:]))
                botcom.specified = int(botcom.specified)
            except ValueError:
                botcom.specified = None
        if botcom.specified:
            botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    # commands that can be updated
    if botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"]:
        if botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"] == "shared":
            adjust_nick_array(bot, str(bot.nick), 'long', 'sayings', botcom.maincom + "_" + str(botcom.responsekey), botcom.dotcommand_dict[botcom.responsekey]["responses"], 'startup')
            botcom.dotcommand_dict[botcom.responsekey]["responses"] = get_nick_value(bot, str(bot.nick), 'long', 'sayings', botcom.dotcommand_dict["validcoms"][0] + "_" + str(botcom.responsekey)) or []
        elif botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"] == "user":
            adjust_nick_array(bot, str(botcom.instigator), 'long', 'sayings', botcom.maincom + "_" + str(botcom.responsekey), botcom.dotcommand_dict[botcom.responsekey]["responses"], 'startup')
            botcom.dotcommand_dict[botcom.responsekey]["responses"] = get_nick_value(bot, str(botcom.instigator), 'long', 'sayings', botcom.dotcommand_dict["validcoms"][0] + "_" + str(botcom.responsekey)) or []

    # Hardcoded commands Below
    if botcom.specified == 'enable':

        if botcom.channel_priv:
            return osd(bot, botcom.instigator, 'notice', "This command must be run in the channel you which to " + botcom.specified + " it in.")

        if botcom.maincom not in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"].keys():
            return osd(bot, botcom.channel_current, 'say', botcom.maincom + " is already " + botcom.specified + "d in " + str(botcom.channel_current))

        if not bot_command_modding_auth(bot, botcom):
            return osd(bot, botcom.channel_current, 'say', "You are not authorized to " + botcom.specified + " " + botcom.maincom + " in " + str(botcom.channel_current))

        del bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"][botcom.maincom]
        osd(bot, botcom.channel_current, 'say', botcom.maincom + " is now " + botcom.specified + "d in " + str(botcom.channel_current))
        botdict_save(bot)
        return

    elif botcom.specified == 'disable':

        if botcom.channel_priv:
            return osd(bot, botcom.instigator, 'notice', "This command must be run in the channel you which to " + botcom.specified + " it in.")

        if botcom.maincom in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"].keys():
            return osd(bot, botcom.channel_current, 'say', botcom.maincom + " is already " + botcom.specified + "d in " + str(botcom.channel_current))

        if not bot_command_modding_auth(bot, botcom):
            return osd(bot, botcom.channel_current, 'say', "You are not authorized to " + botcom.specified + " " + botcom.maincom + " in " + str(botcom.channel_current))

        trailingmessage = spicemanip(bot, botcom.triggerargsarray, 0) or "No reason given."
        timestamp = str(datetime.datetime.utcnow())
        bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"][botcom.maincom] = {"reason": trailingmessage, "timestamp": timestamp, "disabledby": botcom.instigator}
        osd(bot, botcom.channel_current, 'say', botcom.maincom + " is now " + botcom.specified + "d in " + str(botcom.channel_current) + " at " + str(timestamp) + " for the following reason: " + trailingmessage)
        botdict_save(bot)
        return

    elif botcom.specified == 'multiruns':

        if botcom.channel_priv:
            osd(bot, botcom.instigator, 'notice', "This argument must be run in channel.")
            return

        if not bot_command_modding_auth(bot, botcom):
            osd(bot, botcom.channel_current, 'say', "You are not authorized to turn " + botcom.specified + " multicom usage in " + str(botcom.channel_current))
            return

        onoff = spicemanip(bot, botcom.triggerargsarray, 1)
        if onoff == 'on':
            if botcom.maincom not in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["multirun_disabled_commands"].keys():
                osd(bot, botcom.channel_current, 'say', botcom.maincom + " already has multicom usage " + onoff + " in " + str(botcom.channel_current))
            else:
                del bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["multirun_disabled_commands"][botcom.maincom]
                osd(bot, botcom.channel_current, 'say', botcom.maincom + " now has multicom usage " + onoff + " in " + str(botcom.channel_current))
        elif onoff == 'off':
            if botcom.maincom in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["multirun_disabled_commands"].keys():
                osd(bot, botcom.channel_current, 'say', botcom.maincom + " already has multicom usage " + onoff + " in " + str(botcom.channel_current))
            else:
                trailingmessage = spicemanip(bot, botcom.triggerargsarray, "2+") or "No reason given."
                timestamp = str(datetime.datetime.utcnow())
                bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["multirun_disabled_commands"][botcom.maincom] = {"reason": trailingmessage, "timestamp": timestamp, "multi_disabledby": botcom.instigator}
                osd(bot, botcom.channel_current, 'say', botcom.maincom + " now has multicom usage " + onoff + " in " + str(botcom.channel_current))
        else:
            if botcom.maincom not in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["multirun_disabled_commands"].keys():
                osd(bot, botcom.channel_current, 'say', botcom.maincom + " allows multicom use in " + str(botcom.channel_current))
            else:
                osd(bot, botcom.channel_current, 'say', botcom.maincom + " does not allow multicom use in " + str(botcom.channel_current))

        botdict_save(bot)
        return

    elif botcom.specified == 'block':
        botcom.modulerun = False

        if not bot_command_modding_auth(bot, botcom):
            return osd(bot, botcom.channel_current, 'say', "You are not authorized to enable/disable command usage.")

        posstarget = spicemanip(bot, botcom.triggerargsarray, 1) or 0
        if not posstarget:
            return osd(bot, botcom.channel_current, 'say', "Who am I blocking from " + str(botcom.maincom) + " usage?")

        if posstarget not in bot.memory["botdict"]["users"].keys():
            return osd(bot, botcom.channel_current, 'say', "I don't know who " + str(posstarget) + " is.")

        currentblocks = get_nick_value(bot, posstarget, "long", 'commands', "unallowed") or []
        if botcom.maincom in currentblocks:
            return osd(bot, botcom.channel_current, 'say', str(posstarget) + " is already blocked from using " + botcom.maincom + ".")

        adjust_nick_array(bot, posstarget, "long", 'commands', "unallowed", [botcom.maincom], 'add')
        botdict_save(bot)

        return osd(bot, botcom.channel_current, 'say', str(posstarget) + " has been blocked from using " + botcom.maincom + ".")

    elif botcom.specified == 'unblock':
        botcom.modulerun = False

        if not bot_command_modding_auth(bot, botcom):
            return osd(bot, botcom.channel_current, 'say', "You are not authorized to enable/disable command usage.")

        posstarget = spicemanip(bot, botcom.triggerargsarray, 1) or 0
        if not posstarget:
            return osd(bot, botcom.channel_current, 'say', "Who am I unblocking from " + str(botcom.maincom) + " usage?")

        if posstarget not in bot.memory["botdict"]["users"].keys():
            return osd(bot, botcom.channel_current, 'say', "I don't know who " + str(posstarget) + " is.")

        currentblocks = get_nick_value(bot, posstarget, "long", 'commands', "unallowed") or []
        if botcom.maincom not in currentblocks:
            return osd(bot, botcom.channel_current, 'say', str(posstarget) + " is already not blocked from using " + botcom.maincom + ".")

        adjust_nick_array(bot, posstarget, "long", 'commands', "unallowed", [botcom.maincom], 'del')
        botdict_save(bot)

        return osd(bot, botcom.channel_current, 'say', str(posstarget) + " has been unblocked from using " + botcom.maincom + ".")

    elif botcom.specified == 'special':
        nonstockoptions = spicemanip(bot, botcom.nonstockoptions, "andlist")
        return osd(bot, botcom.channel_current, 'say', "The special options for " + str(botcom.maincom) + " command include: " + str(nonstockoptions) + ".")

    elif botcom.specified == 'count':
        return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " command has " + str(len(botcom.dotcommand_dict[botcom.responsekey]["responses"])) + " entries.")

    elif botcom.specified == 'description':
        botcom.modulerun = False

        osd(bot, botcom.channel_current, 'say', str(botcom.specified).title() + ": " + str(botcom.dotcommand_dict["description"]))
        return

    elif botcom.specified == 'exampleresponse':
        botcom.modulerun = False

        osd(bot, botcom.channel_current, 'say', str(botcom.specified).title() + ": " + str(botcom.dotcommand_dict["description"]))
        return

    elif botcom.specified == 'privs':
        botcom.modulerun = False

        osd(bot, botcom.channel_current, 'say', str(botcom.specified).title() + ": " + spicemanip(bot, botcom.dotcommand_dict["privs"], "andlist"))
        return

    elif botcom.specified in ['example', 'usage']:
        botcom.modulerun = False

        osd(bot, botcom.channel_current, 'say', str(botcom.specified).title() + ": " + str(botcom.dotcommand_dict["description"]))
        return

    elif botcom.specified == 'filepath':
        return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " file is located at " + str(botcom.dotcommand_dict["filepath"]))

    elif botcom.specified == 'author':
        return osd(bot, botcom.channel_current, 'say', "The author of the " + str(botcom.maincom) + " command is " + botcom.dotcommand_dict["author"] + ".")

    elif botcom.specified in ['contrib', "contributors"]:
        return osd(bot, botcom.channel_current, 'say', "The contributors of the " + str(botcom.maincom) + " command are " + spicemanip(bot, botcom.dotcommand_dict["contributors"], "andlist") + ".")

    elif botcom.specified == 'alias':
        return osd(bot, botcom.channel_current, 'say', "The alaises of the " + str(botcom.maincom) + " command are " + spicemanip(bot, botcom.dotcommand_dict["validcoms"], "andlist") + ".")

    elif botcom.specified == 'view':
        if botcom.dotcommand_dict[botcom.responsekey]["responses"] == []:
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " command appears to have no entries!")
        else:
            osd(bot, botcom.instigator, 'notice', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " command contains:")
            listnumb, relist = 1, []
            for item in botcom.dotcommand_dict[botcom.responsekey]["responses"]:
                if listnumb <= 20:
                    if isinstance(item, dict):
                        relist.append(str("[#" + str(listnumb) + "] COMPLEX dict Entry"))
                    elif isinstance(item, list):
                        relist.append(str("[#" + str(listnumb) + "] COMPLEX list Entry"))
                    else:
                        relist.append(str("[#" + str(listnumb) + "] " + str(item)))
                listnumb += 1
            osd(bot, botcom.instigator, 'say', relist)
            if listnumb > 20:
                osd(bot, botcom.instigator, 'say', "List cut off after the 20th entry to prevent bot lag.")
            return

    elif botcom.specified == 'add':

        if not botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"]:
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list cannot be updated.")

        fulltext = spicemanip(bot, botcom.triggerargsarray, 0)
        if not fulltext:
            return osd(bot, botcom.channel_current, 'say', "What would you like to add to the " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list?")

        if fulltext in botcom.dotcommand_dict[botcom.responsekey]["responses"]:
            return osd(bot, botcom.channel_current, 'say', "The following was already in the " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list: '" + str(fulltext) + "'")

        if botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"] == "shared":
            adjust_nick_array(bot, str(bot.nick), 'long', 'sayings', botcom.maincom + "_" + str(botcom.responsekey), fulltext, botcom.specified)
        elif botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"] == "user":
            adjust_nick_array(bot, str(botcom.instigator), 'long', 'sayings', botcom.maincom + "_" + str(botcom.responsekey), fulltext, botcom.specified)

        return osd(bot, botcom.channel_current, 'say', "The following was added to the " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list: '" + str(fulltext) + "'")

    elif botcom.specified in ['del', 'remove']:

        if not botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"]:
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list cannot be updated.")

        fulltext = spicemanip(bot, botcom.triggerargsarray, 0)
        if not fulltext:
            return osd(bot, botcom.channel_current, 'say', "What would you like to remove from the " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list?")

        if fulltext not in botcom.dotcommand_dict[botcom.responsekey]["responses"]:
            return osd(bot, botcom.channel_current, 'say', "The following was already not in the " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list: '" + str(fulltext) + "'")

        if botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"] == "shared":
            adjust_nick_array(bot, str(bot.nick), 'long', 'sayings', botcom.maincom + "_" + str(botcom.responsekey), fulltext, botcom.specified)
        elif botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"] == "user":
            adjust_nick_array(bot, str(botcom.instigator), 'long', 'sayings', botcom.maincom + "_" + str(botcom.responsekey), fulltext, botcom.specified)

        return osd(bot, botcom.channel_current, 'say', "The following was removed from the " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list: '" + str(fulltext) + "'")

    elif botcom.specified and not botcom.dotcommand_dict[botcom.responsekey]["selection_allowed"]:
        return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " response list cannot be specified.")

    botcom.target = False

    currentblocks = get_nick_value(bot, botcom.instigator, "long", 'commands', "unallowed") or []
    if botcom.maincom in currentblocks:
        return osd(bot, botcom.channel_current, 'say', "You appear to have been blocked by a bot admin from using the " + botcom.maincom + " command.")

    if not botcom.channel_priv:

        if botcom.maincom in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"].keys():
            reason = bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"][str(botcom.maincom)]["reason"]
            timestamp = bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"][str(botcom.maincom)]["timestamp"]
            bywhom = bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"][str(botcom.maincom)]["disabledby"]
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " command was disabled by " + bywhom + " in " + str(botcom.channel_current) + " at " + str(timestamp) + " for the following reason: " + str(reason))

    # hardcoded_channel_block
    if not botcom.channel_priv:
        if str(botcom.channel_current) in botcom.dotcommand_dict["hardcoded_channel_block"]:
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " command cannot be used in " + str(botcom.channel_current) + " because it is hardcoded not to.")

    # hardcoded_channel_block
    if not botcom.channel_priv:
        if str(botcom.channel_current) in botcom.dotcommand_dict[botcom.responsekey]["hardcoded_channel_block"]:
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " command cannot be used in " + str(botcom.channel_current) + " because it is hardcoded not to.")

    botcom.success = True
    if botcom.commandtype in ['simple', 'fillintheblank', "target", 'targetplusreason', 'sayings', "readfromfile", "readfromurl", "ascii_art", "translate", "responses"]:
        return bot_dictcom_responses(bot, botcom)
    else:
        command_function_run = str('bot_dictcom_' + botcom.commandtype + '(bot, botcom)')
        eval(command_function_run)


def bot_dictcom_responses(bot, botcom):

    commandrunconsensus = []
    reaction = False

    # A target is required
    if botcom.dotcommand_dict[botcom.responsekey]["target_required"]:

        # try first term as a target
        posstarget = spicemanip(bot, botcom.triggerargsarray, 1) or 0
        targetbypass = botcom.dotcommand_dict[botcom.responsekey]["target_bypass"]
        targetchecking = bot_target_check(bot, botcom, posstarget, targetbypass)
        if not targetchecking["targetgood"]:

            if botcom.dotcommand_dict[botcom.responsekey]["target_backup"]:
                botcom.target = botcom.dotcommand_dict[botcom.responsekey]["target_backup"]
                if botcom.target == 'instigator':
                    botcom.target = botcom.instigator
                elif botcom.target == 'random':
                    botcom.target = bot_random_valid_target(bot, botcom, 'random')
            else:
                for reason in ['self', 'bot', 'bots', 'offline', 'unknown', 'privmsg', 'diffchannel', 'diffbot']:
                    if targetchecking["reason"] == reason and botcom.dotcommand_dict[botcom.responsekey]["react_"+reason]:
                        reaction = True
                        commandrunconsensus.append(botcom.dotcommand_dict[botcom.responsekey]["react_"+reason])
                if not reaction:
                    commandrunconsensus.append([targetchecking["error"]])
        else:
            botcom.target = spicemanip(bot, botcom.triggerargsarray, 1)
            botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    # $blank input
    botcom.completestring = spicemanip(bot, botcom.triggerargsarray, 0) or ''
    if botcom.dotcommand_dict[botcom.responsekey]["blank_required"]:

        if botcom.completestring == '' or not botcom.completestring:

            if botcom.dotcommand_dict[botcom.responsekey]["blank_backup"]:
                botcom.completestring = botcom.dotcommand_dict[botcom.responsekey]["blank_backup"]
            else:
                commandrunconsensus.append(botcom.dotcommand_dict[botcom.responsekey]["blank_fail"])

        if botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"]:
            if botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"] != []:
                if spicemanip(bot, botcom.completestring, 1).lower() not in botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"]:
                    botcom.completestring = botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"][0] + " " + botcom.completestring
                elif spicemanip(bot, botcom.completestring, 1).lower() in botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"]:
                    if spicemanip(bot, botcom.completestring, 1).lower() != botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"][0]:
                        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
                        if botcom.triggerargsarray != []:
                            botcom.completestring = botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"][0] + " " + spicemanip(bot, botcom.triggerargsarray, 0)

    if commandrunconsensus != []:
        botcom.success = False
        if botcom.dotcommand_dict[botcom.responsekey]["response_fail"] and not reaction:
            botcom.dotcommand_dict[botcom.responsekey]["responses"] = botcom.dotcommand_dict[botcom.responsekey]["response_fail"]
        else:
            botcom.dotcommand_dict[botcom.responsekey]["responses"] = commandrunconsensus[0]

    bot_dictcom_reply_shared(bot, botcom)


def bot_dictcom_reply_shared(bot, botcom):

    if botcom.specified:
        if botcom.specified > len(botcom.dotcommand_dict[botcom.responsekey]["responses"]):
            currentspecified = len(botcom.dotcommand_dict[botcom.responsekey]["responses"])
        else:
            currentspecified = botcom.specified
        botcom.replies = spicemanip(bot, botcom.dotcommand_dict[botcom.responsekey]["responses"], currentspecified, 'return')
    else:
        botcom.replies = spicemanip(bot, botcom.dotcommand_dict[botcom.responsekey]["responses"], 'random', 'return')

    # This handles responses in list form
    if not isinstance(botcom.replies, list):
        botcom.replies = [botcom.replies]

    for rply in botcom.replies:

        # replies that can be evaluated as code
        if rply.startswith("time.sleep"):
            eval(rply)
        else:

            # random number
            if "$randnum" in rply:
                if botcom.dotcommand_dict[botcom.responsekey]["randnum"]:
                    randno = randint(botcom.dotcommand_dict[botcom.responsekey]["randnum"][0], botcom.dotcommand_dict[botcom.responsekey]["randnum"][1])
                else:
                    randno = randint(0, 50)
                rply = rply.replace("$randnum", str(randno))

            # blank
            if "$blank" in rply:
                rply = rply.replace("$blank", botcom.completestring or '')

            # the remaining input
            if "$input" in rply:
                rply = rply.replace("$input", spicemanip(bot, botcom.triggerargsarray, 0) or botcom.maincom)

            # translation
            if botcom.dotcommand_dict[botcom.responsekey]["translations"]:
                rply = bot_translate_process(bot, rply, botcom.dotcommand_dict[botcom.responsekey]["translations"])

            # text to precede the output
            if botcom.dotcommand_dict[botcom.responsekey]["prefixtext"] and botcom.success:
                rply = spicemanip(bot, botcom.dotcommand_dict[botcom.responsekey]["prefixtext"], 'random') + rply

            # text to follow the output
            if botcom.dotcommand_dict[botcom.responsekey]["suffixtext"] and botcom.success:
                rply = rply + spicemanip(bot, botcom.dotcommand_dict[botcom.responsekey]["suffixtext"], 'random')

            # trigger.nick
            if "$instigator" in rply:
                rply = rply.replace("$instigator", botcom.instigator or '')

            # random user
            if "$randuser" in rply:
                if not botcom.channel_priv:
                    randuser = spicemanip(bot, bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['current_users'], 'random')
                else:
                    randuser = botcom.instigator
                rply = rply.replace("$randuser", randuser)

            # current channel
            if "$channel" in rply:
                rply = rply.replace("$channel", botcom.channel_current or '')

            # current channel
            if "$server" in rply:
                rply = rply.replace("$server", botcom.server or '')

            # bot.nick
            if "$botnick" in rply:
                rply = rply.replace("$botnick", bot.nick or '')

            # target
            if "$target" in rply:
                targetnames = botcom.target or ''
                if "$targets" in rply:
                    if targetnames.lower() == "your":
                        targetnames = targetnames
                    elif targetnames.endswith("s"):
                        targetnames = targetnames + "'"
                    else:
                        targetnames = targetnames + "s"
                    rply = rply.replace("$targets", targetnames)
                else:
                    targetnames = targetnames
                    rply = rply.replace("$target", targetnames)

            # smaller variations for the text
            if "$replyvariation" in rply:
                if botcom.dotcommand_dict[botcom.responsekey]["replyvariation"] != []:
                    variation = spicemanip(bot, botcom.dotcommand_dict[botcom.responsekey]["replyvariation"], 'random')
                    rply = rply.replace("$replyvariation", variation)
                else:
                    rply = rply.replace("$replyvariation", '')

            # display special options for this command
            if "$specialoptions" in rply:
                nonstockoptions = []
                for command in botcom.dotcommand_dict.keys():
                    if command not in ["?default", "validcoms", "contributors", "author", "type", "filepath", "hardcoded_channel_block", "description", "exampleresponse", "example", "usage", "privs"]:
                        nonstockoptions.append(command)
                nonstockoptions = spicemanip(bot, nonstockoptions, "andlist")
                rply = rply.replace("$specialoptions", nonstockoptions)

            # saying, or action?
            if rply.startswith("*a "):
                rplytype = 'action'
                rply = rply.replace("*a ", "")
            else:
                rplytype = 'say'

            osd(bot, botcom.channel_current, rplytype, rply)


def bot_dictcom_gif(bot, botcom):

    if botcom.dotcommand_dict[botcom.responsekey]["blank_required"] and not botcom.completestring:
        botcom.dotcommand_dict[botcom.responsekey]["responses"] = botcom.dotcommand_dict[botcom.responsekey]["blank_fail"]
        return bot_dictcom_reply_shared(bot, botcom)
    elif botcom.dotcommand_dict[botcom.responsekey]["blank_required"] and botcom.completestring:
        queries = [botcom.completestring]
    else:
        queries = botcom.dotcommand_dict[botcom.responsekey]["responses"]

    # which api's are we using to search
    if botcom.dotcommand in bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'].keys():
        searchapis = [botcom.dotcommand]
    elif "queryapi" in botcom.dotcommand_dict.keys():
        searchapis = botcom.dotcommand_dict[botcom.responsekey]["queryapi"]
    else:
        searchapis = bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'].keys()

    if botcom.specified:
        if botcom.specified > len(queries):
            botcom.specified = len(queries)
        query = spicemanip(bot, queries, botcom.specified, 'return')
    else:
        query = spicemanip(bot, queries, 'random', 'return')

    searchdict = {"query": query, "gifsearch": searchapis}

    # nsfwenabled = get_database_value(bot, bot.nick, 'channels_nsfw') or []
    # if botcom.channel_current in nsfwenabled:
    #    searchdict['nsfw'] = True

    gifdict = getGif(bot, searchdict)

    if gifdict["error"]:
        botcom.success = False
        if botcom.dotcommand_dict[botcom.responsekey]["search_fail"]:
            gifdict["error"] = botcom.dotcommand_dict[botcom.responsekey]["search_fail"]
        botcom.dotcommand_dict[botcom.responsekey]["responses"] = [gifdict["error"]]
    else:
        botcom.dotcommand_dict[botcom.responsekey]["responses"] = [str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"]))]

    botcom.specified = False
    bot_dictcom_reply_shared(bot, botcom)


def bot_dictcom_feeds(bot, botcom):

    feed = botcom.dotcommand_dict[botcom.responsekey]["responses"][0]
    if feed not in bot.memory["botdict"]["tempvals"]['feeds'].keys():
        return osd(bot, botcom.channel_current, 'say', feed + " does not appear to be a valid feed.")

    dispmsg = bot_dictcom_feeds_handler(bot, feed, True)
    if dispmsg == []:
        osd(bot, botcom.channel_current, 'say', feed + " appears to have had an unknown error.")
    else:
        osd(bot, botcom.channel_current, 'say', dispmsg)


def bot_dictcom_search(bot, botcom):
    bot.say("testing done")
