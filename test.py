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
    topic = trigger.args[1]
    bot.say(str(topic))
