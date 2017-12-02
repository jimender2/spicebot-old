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
    fullstring = trigger.group(2)
    numberofwords = len(fullstring.split())
    argone = triggerargsnumber(fullstring, 1)
    bot.say(str(argone))
    bot.day(str(numberofwords))


#def settheargvars():
    

def triggerargsnumber(fullstring, number):
    triggerargsarray = []
    number = number - 1
    for word in fullstring.split():
        triggerargsarray.append(word)
    entriestotal = len(triggerargsarray)
    try:
        triggerarg = triggerargsarray[number]
    except IndexError:
        triggerarg = "ERROROUTOFRANGE"
    return triggerarg




