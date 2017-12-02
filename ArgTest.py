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
    argone = triggerargsnumber(fullcommandused, 0)
    argeleven = triggerargsnumber(fullcommandused, 1)
    argtwelve = triggerargsnumber(fullcommandused, 2)
    bot.say(str(fullcommandused))
    bot.say(str(argone))
    bot.say(str(argeleven))
    bot.say(str(argtwelve))
    
def triggerargsnumber(fullcommandused, number):
    triggerargsarray = []
    for word in fullcommandused.split():
        triggerargsarray.append(word)
    entriestotal = len(triggerargsarray)
    triggerarg = triggerargsarray[number] or 8675309
    return triggerarg




