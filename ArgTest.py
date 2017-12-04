import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.require_admin
@sopel.module.commands('argtest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    newvalue = get_trigger_arg(triggerargsarray, '5+')
    newvalueb = get_trigger_arg(triggerargsarray, '5-')
    newvaluec = get_trigger_arg(triggerargsarray, '5<')
    newvalued = get_trigger_arg(triggerargsarray, '5>')
    newvaluee = get_trigger_arg(triggerargsarray, 'last')
    newvaluef = get_trigger_arg(triggerargsarray, '5^7')
    totalarray = len(triggerargsarray)
    totalarray = totalarray + 1
    for i in range(0,totalarray):
        arg = get_trigger_arg(triggerargsarray, i)
        bot.say("arg" + str(i) + " = " + str(arg))
    if newvalue != '':
        bot.say("simulating arg5+ " + str(newvalue))
    else:
        bot.say("can't simulate 5+ as it returns empty values.")
    if newvalueb != '':
        bot.say("simulating arg5- " + str(newvalueb))
    else:
        bot.say("can't simulate 5- as it returns empty values.")
    if newvaluec != '':
        bot.say("simulating arg5< " + str(newvaluec))
    else:
        bot.say("can't simulate 5< as it returns empty values.")
    if newvalued != '':
        bot.say("simulating arg5> " + str(newvalued))
    else:
        bot.say("can't simulate 5> as it returns empty values.")
    if newvaluee != '':
        bot.say("simulating arg last " + str(newvaluee))
    else:
        bot.say("can't simulate arg last as it returns empty values.")
    if newvaluef != '':
        bot.say("simulating arg 5^7 " + str(newvaluef))
    else:
        bot.say("can't simulate arg 5^7 as it returns empty values.")
