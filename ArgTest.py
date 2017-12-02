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
    triggerargsarray = create_args_array(fullstring)
    numberofwords = number_of_words(triggerargsarray)
    argone = get_trigger_arg(triggerargsarray, 1)
    argtwelve = get_trigger_arg(triggerargsarray, 12)
    bot.say(str(argone))
    bot.say(str(argtwelve))
    bot.day(str(numberofwords))

def create_args_array(fullstring):
    triggerargsarray = []
    for word in fullstring.split():
        triggerargsarray.append(word)
    return triggerargsarray

def number_of_words(triggerargsarray):
    entriestotal = len(triggerargsarray)
    return entriestotal

def get_trigger_arg(triggerargsarray, number):
    number = number - 1
    try:
        triggerarg = triggerargsarray[number]
    except IndexError:
        triggerarg = ''
    return triggerarg





