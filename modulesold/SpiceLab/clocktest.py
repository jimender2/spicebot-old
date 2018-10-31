from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel import module, tools
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('testclock')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    commandused = spicemanip(bot, triggerargsarray, 1)
    if commandused == 'on':
        set_database_value(bot, bot.nick, 'testclock', 1)
    elif commandused == 'off':
        set_database_value(bot, bot.nick, 'testclock', 0)
    elif commandused == 'check':
        currentsetting = get_database_value(bot, bot.nick, 'testclock')
        osd(bot, trigger.sender, 'say', str(currentsetting))


@sopel.module.interval(15)
def countdown(bot):
    currentsetting = get_database_value(bot, bot.nick, 'testclock')
    if currentsetting == 1:
        channel = '##spicebottest'
        dispmsg = '15 secs have passed'
        osd(bot, trigger.sender, 'say', dispmsg)