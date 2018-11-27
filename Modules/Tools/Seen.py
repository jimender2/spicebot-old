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


@module.rule('.*')
@module.intent('ACTION')
@sopel.module.thread(True)
def duel_action(bot, trigger):

    for triggertest in ["", ".sender", ".time", ".raw", ".is_privmsg", ".hostmask", ".user", ".nick", ".event", ".match", ".group(0)", ".groups", ".groupdict", ".args", ".tags", ".admin", ".owner", ".account"]:
        try:
            dispvalue = str(eval("trigger" + triggertest))
        except Exception as e:
            dispvalue = str(e)
        bot.msg("#spicebottest", str(triggertest) + "     " + str(dispvalue))

    return
    if 'intent' in trigger.tags:
        if trigger.tags['intent'] == 'ACTION':
            maincom = str(trigger.group(0))
        else:
            maincom = str(trigger.group(0))
    else:
        maincom = str(trigger.group(0))
    bot.msg("#spicebottest", str(maincom))


@sopel.module.commands('seendev')
@sopel.module.thread(True)
def seen(bot, trigger):

    # for triggertest in ["", "._callables['high']", "._callables['medium']", "._callables['low']", ".config", ".doc", "._command_groups", ".stats", ".times", ".server_capabilities", ".enabled_capabilities", "._cap_reqs", ".privileges", ".channels", ".users", ".db", ".shutdown_methods"]:
    for triggertest in [".ops", ".halfplus", ".voices"]:
        try:
            dispvalue = str(eval("bot" + triggertest))
        except Exception as e:
            dispvalue = str(e)
        bot.msg("#spicebottest", str(triggertest))
        bot.msg("#spicebottest", "     " + str(dispvalue))

    return

    # don't run jobs if not ready
    while "botdict_loaded" not in bot.memory:
        time.sleep(1)

    return

    nick = trigger.group(3)
    if not nick:
        osd(bot, trigger.sender, 'say', ".seen <nick> - Reports when <nick> was last seen.")


def bot_module_prerun(bot, trigger):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # what time was this triggered
    botcom.timestart = trigger.time

    # default if module will run
    botcom.modulerun = True

    # instigator
    botcom.instigator = str(trigger.nick)
    botcom.instigator_hostmask = str(trigger.hostmask)
    botcom.instigator_user = str(trigger.user)

    # bot credentials
    botcom.admin = trigger.admin
    botcom.owner = trigger.owner

    # channel
    botcom.channel_current = str(trigger.sender)
    botcom.channel_priv = trigger.is_privmsg

    # channel creds
    for privtype in ['VOICE', 'HALFOP', 'OP', 'ADMIN', 'OWNER']:
        privstring = str("chan" + privtype.lower() + "s")
        evalstring = str("bot.memory['botdict']['tempvals']['channels_list']['" + botcom.channel_current + "']['" + privstring + "']")
        if botcom.instigator in eval(evalstring):
            createuserdict = str("botcom." + privtype + " = True")
        else:
            createuserdict = str("botcom." + privtype + " = False")
        exec(createuserdict)

    # Bots can't run commands
    if botcom.instigator in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
        return

    botcom.dotcommand = spicemanip(bot, botcom.triggerargsarray, 1).lower()[1:]

    # the command that was run
    if 'intent' not in trigger.tags:
        botcom.maincom = str(trigger.group(1))
    else:
        botcom.maincom = str(trigger.group(1))

    # create arg list
    botcom.triggerargsarray = spicemanip(bot, trigger, 'create')

    # This allows users to specify which reply by number by using an ! and a digit (first or last in string)
    validspecifides = []
    botcom.specified = None
    argone = spicemanip(bot, botcom.triggerargsarray, 1)
    if str(argone).startswith("--") and len(str(argone)) > 2:
        if str(argone[2:]).isdigit() or str(argone[2:]) in validspecifides:
            botcom.specified = argone[2:]
        else:
            try:
                botcom.specified = w2n.word_to_num(str(argone[1:]))
            except ValueError:
                botcom.specified = None
        if botcom.specified:
            botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    if botcom.specified:
        if str(botcom.specified).isdigit():
            botcom.specified = int(botcom.specified)

    # Hardcoded commands Below
    if botcom.specified == 'enable':
        botcom.modulerun = False

        if botcom.channel_priv:
            osd(bot, botcom.instigator, 'notice', "This command must be run in the channel you which to " + botcom.specified + " it in.")
            return botcom

        if botcom.maincom not in bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"].keys():
            osd(bot, botcom.channel_current, 'say', botcom.maincom + " is already " + botcom.specified + "d in " + str(botcom.channel_current))
            return botcom

        commandrunconsensus, commandrun = [], True
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['bot_admins']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanops']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanowners']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanadmins']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if 'True' not in commandrunconsensus:
            commandrun = False
        if not commandrun:
            osd(bot, botcom.channel_current, 'say', "You are not authorized to " + botcom.specified + " " + botcom.maincom + " in " + str(botcom.channel_current))
            return botcom

        del bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"][botcom.maincom]
        osd(bot, botcom.channel_current, 'say', botcom.maincom + " is now " + botcom.specified + "d in " + str(botcom.channel_current))
        return botcom

    elif botcom.specified == 'disable':
        botcom.modulerun = False

        if botcom.channel_priv:
            osd(bot, botcom.instigator, 'notice', "This command must be run in the channel you which to " + botcom.specified + " it in.")
            return botcom

        if botcom.maincom in bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"].keys():
            osd(bot, botcom.channel_current, 'say', botcom.maincom + " is already " + botcom.specified + "d in " + str(botcom.channel_current))
            return botcom

        commandrunconsensus, commandrun = [], True
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['bot_admins']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanops']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanowners']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanadmins']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if 'True' not in commandrunconsensus:
            commandrun = False
        if not commandrun:
            osd(bot, botcom.channel_current, 'say', "You are not authorized to " + botcom.specified + " " + botcom.maincom + " in " + str(botcom.channel_current))
            return botcom

        if not botcom.channel_priv:
            if botcom.maincom in bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"].keys():
                reason = bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"][str(botcom.maincom)]["reason"]
                timestamp = bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"][str(botcom.maincom)]["timestamp"]
                bywhom = bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"][str(botcom.maincom)]["disabledby"]
                osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " command was disabled by " + bywhom + " in " + str(botcom.channel_current) + " at " + str(timestamp) + " for the following reason: " + str(reason))
                return botcom

    return botcom
