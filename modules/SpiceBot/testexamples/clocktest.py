from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel import module, tools
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('testclock')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)


def execute_main(bot, trigger, triggerargsarray):
    commandused = get_trigger_arg(bot, triggerargsarray,1)
    if commandused == 'on':
        set_database_value(bot,bot.nick,'testclock',1)
    elif commandused == 'off':
        set_database_value(bot,bot.nick,'testclock',0)
    elif commandused == 'check':
        currentsetting = get_database_value(bot,bot.nick,'testclock')
        bot.say(str(currentsetting))


@sopel.module.interval(15)
def countdown(bot):
    currentsetting = get_database_value(bot,bot.nick,'testclock')
    if currentsetting == 1:
        channel = '##spicebottest'
        dispmsg = '15 secs have passed'
        onscreentext(bot, channel, dispmsg)
