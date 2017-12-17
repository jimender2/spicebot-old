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
def automodspam(bot, trigger):
    channel = trigger.sender
    instigator = trigger.nick
    if not trigger.is_privmsg:
        lastnicksubmit = get_botdatabase_value(bot, channel, 'automod_antifloodnick') or bot.nick
        if lastnicksubmit != instigator:
            set_botdatabase_value(bot, channel, 'automod_antifloodnick', instigator)
            set_botdatabase_value(bot, channel, 'automod_antifloodcount', 1)
        else:
            adjust_botdatabase_value(bot, channel, 'automod_antifloodcount', 1)
            getcurrentcount = get_botdatabase_value(bot, channel, 'automod_antifloodcount') or 1
            bot.msg(channel,str(getcurrentcount))
        
    
    #    if lastnicksubmit = instigator:
    #        adjust_botdatabase_value(bot, channel, 'automod_antifloodcount', 1)
    #        lastnicksubmitcount = get_botdatabase_value(bot, channel, 'automod_antifloodcount')
    #        if lastnicksubmitcount >= 5:
    #            lastnicksubmitwarned = get_botdatabase_value(bot, channel, 'automod_antifloodnickwarned')
    #            if lastnicksubmitwarned != instigator:
    #                set_botdatabase_value(bot, channel, 'automod_antifloodnickwarned', instigator)
    #                yellatyoumsg = str(instigator + ", Please do not flood the channel.")
    #                bot.msg(channel,yellatyoumsg)
    #    else:
    #        set_botdatabase_value(bot, channel, 'automod_antifloodcount', 1)
    #        set_botdatabase_value(bot, channel, 'automod_antifloodnick', instigator)
    #        set_botdatabase_value(bot, channel, 'automod_antifloodnickwarned', None)
