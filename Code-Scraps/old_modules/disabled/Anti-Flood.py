#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@thread(False)
@rule('(.*)')
@priority('low')
def antiflood(bot, trigger):
    instigator = trigger.nick
    if not trigger.is_privmsg and instigator != bot.nick and not bot.nick.endswith(devbot):
        # vars
        channel = trigger.sender
        currentmessage = trigger.group(1)

        # Flooding is 5 lines in a row by the same person or 3 identical lines
        floodyell = 0
        antifloodwarning = str(instigator + ", please do not flood the channel.")
        lastnicksubmit = get_database_value(bot, channel, 'automod_antifloodnick') or bot.nick
        if lastnicksubmit != instigator:
            set_database_value(bot, channel, 'automod_antifloodnick', instigator)
            set_database_value(bot, channel, 'automod_antifloodcount', 1)
            set_database_value(bot, channel, 'automod_antifloodnickwarned', None)
            set_database_value(bot, channel, 'automod_antifloodmessage', currentmessage)
            set_database_value(bot, channel, 'automod_antifloodmessagecount', 1)
        else:
            lastmessage = get_database_value(bot, channel, 'automod_antifloodmessage') or ''
            if currentmessage != lastmessage:
                set_database_value(bot, channel, 'automod_antifloodmessage', currentmessage)
                set_database_value(bot, channel, 'automod_antifloodmessagecount', 1)
            else:
                adjust_database_value(bot, channel, 'automod_antifloodmessagecount', 1)
                getcurrentmessagecount = get_database_value(bot, channel, 'automod_antifloodmessagecount') or 1
                if int(getcurrentmessagecount) >= 3:
                    floodyell = 1
            lastnicksubmit = get_database_value(bot, channel, 'automod_antifloodnick') or bot.nick
            adjust_database_value(bot, channel, 'automod_antifloodcount', 1)
            getcurrentcount = get_database_value(bot, channel, 'automod_antifloodcount') or 1
            if int(getcurrentcount) > 5:
                floodyell = 1
        lastnicksubmitwarned = get_database_value(bot, channel, 'automod_antifloodnickwarned') or bot.nick
        if lastnicksubmitwarned != instigator and floodyell:
            set_database_value(bot, channel, 'automod_antifloodnickwarned', instigator)
            osd(bot, channel, 'action', antifloodwarning)
