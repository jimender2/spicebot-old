from __future__ import unicode_literals, absolute_import, print_function, division
import time
import datetime
from sopel.tools import Identifier
from sopel.tools.time import get_timezone, format_time
from sopel.module import commands, rule, priority, thread
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@thread(False)
@rule('(.*)')
@priority('low')
def automod(bot, trigger):
    if not trigger.is_privmsg:
        
        floodyell = 0
        antifloodwarning = str(instigator + ", please do not flood the channel.")
        
        channel = trigger.sender
        instigator = trigger.nick
        currentmessage = trigger.group(2)

        ## Flooding is 5 lines in a row by the same person or 3 identical lines
        lastnicksubmit = get_botdatabase_value(bot, channel, 'automod_antifloodnick') or bot.nick
        if lastnicksubmit != instigator:
            set_botdatabase_value(bot, channel, 'automod_antifloodnick', instigator)
            set_botdatabase_value(bot, channel, 'automod_antifloodcount', 1)
            set_botdatabase_value(bot, channel, 'automod_antifloodnickwarned', None)
            set_botdatabase_value(bot, channel, 'automod_antifloodmessage', currentmessage)
            set_botdatabase_value(bot, channel, 'automod_antifloodmessagecount', 1)
        else:
            lastmessage = get_botdatabase_value(bot, channel, 'automod_antifloodmessage') or ''
            if currentmessage != lastmessage:
                set_botdatabase_value(bot, channel, 'automod_antifloodmessage', currentmessage)
                set_botdatabase_value(bot, channel, 'automod_antifloodmessagecount', 1)
            else:
                adjust_botdatabase_value(bot, channel, 'automod_antifloodmessagecount', 1)
                getcurrentmessagecount = get_botdatabase_value(bot, channel, 'automod_antifloodmessagecount') or 1
                if int(getcurrentmessagecount) >= 3:
                    floodyell = 1
            lastnicksubmit = get_botdatabase_value(bot, channel, 'automod_antifloodnick') or bot.nick
            adjust_botdatabase_value(bot, channel, 'automod_antifloodcount', 1)
            getcurrentcount = get_botdatabase_value(bot, channel, 'automod_antifloodcount') or 1
            if int(getcurrentcount) >= 5:
                lastnicksubmitwarned = get_botdatabase_value(bot, channel, 'automod_antifloodnickwarned') or bot.nick
                if lastnicksubmitwarned != instigator:
                    set_botdatabase_value(bot, channel, 'automod_antifloodnickwarned', instigator)
                    floodyell = 1 
        if floodyell:
            bot.msg(channel,antifloodwarning)
        

