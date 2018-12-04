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


@rule('.*')
@sopel.module.thread(True)
@sopel.module.interval(1800)
def watch_all_hub(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["connected", "botdict", "server", "channels", "users"]):
        pass

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # what time was this triggered
    botcom.timestart = time.time()

    # instigator
    botcom.instigator = str(trigger.nick)
    botcom.instigator_hostmask = str(trigger.hostmask)
    botcom.instigator_user = str(trigger.user)

    # bot credentials
    botcom.admin = trigger.admin
    botcom.owner = trigger.owner

    # server
    botcom.server = bot.memory["botdict"]["tempvals"]['server']

    # channel
    botcom.channel_current = str(trigger.sender)
    botcom.channel_priv = trigger.is_privmsg

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    # channel creds
    for privtype in ['VOICE', 'HALFOP', 'OP', 'ADMIN', 'OWNER']:
        if not botcom.channel_priv:
            privstring = str("chan" + privtype.lower() + "s")
            evalstring = str("bot.memory['botdict']['tempvals']['servers_list'][" + str(botcom.server) + "]['channels_list']['" + botcom.channel_current + "']['" + privstring + "']")
            grouplist = eval(evalstring)
        else:
            grouplist = []
        if botcom.instigator in grouplist:
            createuserdict = str("botcom." + privtype + " = True")
        else:
            createuserdict = str("botcom." + privtype + " = False")
        exec(createuserdict)

    # what they said
    botcom.triggerargsarray = spicemanip(bot, trigger, 'create')

    if botcom.channel_priv:
        return

    botcom.timestart = time.time()

    spoken = spicemanip(bot, botcom.triggerargsarray, 0)
    if 'all' not in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["auth_block"]:
        spoken = "***********"

    usertalkdict = {
                    "server": str(bot.memory["botdict"]["tempvals"]['servername']),
                    "channel": botcom.channel_current,
                    "spoken": spoken,
                    "time": botcom.timestart,
                    "bot_eyes": str(bot.nick),
                    "intent": 'intent' in trigger.tags,
                    }

    currentnickrecord = get_nick_value(bot, botcom.instigator, 'long', 'user_activity', 'list') or []
    currentnickrecord.append(usertalkdict)
    if len(currentnickrecord) > 10:
        del currentnickrecord[0]

    set_nick_value(bot, botcom.instigator, 'long', 'user_activity', 'list', currentnickrecord)
