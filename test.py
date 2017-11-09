# -*- coding: utf-8 -*/
from sopel import module
from sopel.tools import events
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('test')
def mainfunction(bot, trigger):
    args = trigger.args[1]
    one = trigger.group(1)
    two = trigger.group(2)
    three = trigger.group(3)
    four = trigger.group(4)
    five = trigger.group(5)
    bot.say("args = " + str(args))
    bot.say("one = " + str(one))
    bot.say("two = " + str(two))
    bot.say("three = " + str(three))
    bot.say("four = " + str(four))
    bot.say("five = " + str(five))
