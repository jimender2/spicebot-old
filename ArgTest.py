# -*- coding: utf-8 -*/
from sopel import module
from sopel.tools import events
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.require_admin
@sopel.module.commands('argtest')
def mainfunction(bot, trigger):
    fullcommandused = trigger.group(2)
    argone = fullcommandused.triggerargsnumber(0)
    bot.say(str(fullcommandused))
    bot.say(str(argone))
    
def triggerargsnumber(number):
    triggerargsarray = []
    for word in fullcommandused.split():
        triggerargsarray.append(word)
    entriestotal = len(triggerargsarray)
    #if number <= entriestotal:
    #    triggerarg = triggerargsarray[arraynumber] or 0
    #else:
    #    triggerarg = 0
    triggerarg = triggerargsarray[arraynumber] or ''
    return triggerarg




