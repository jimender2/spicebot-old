#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('drugs')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):

    locationorperson = get_trigger_arg(bot,triggerargsarray,'1+')
    person = trigger.nick
    druglocation = "somewhere tropical"
    drugdisplay = "to " + druglocation
    displaymsg = "Whoops, something went wrong. Not sure how that got fucked up."

    # Nothing special
    if not locationorperson:
        displaymsg = person + " contemplates selling everything and moving " + drugdisplay + " to sell drugs on a beach."

    # Someone specified
    elif locationorperson.lower() in [u.lower() for u in bot.users]:
        person = locationorperson
        druglocation = get_trigger_arg(bot,triggerargsarray,'2+')
        displaymsg = person + " should really consider selling everything and moving " + drugdisplay + " to sell drugs on a beach."

    # Location specified
    else:
        druglocation = locationorperson
        drugdisplay = "to " + druglocation
        displaymsg = person + " contemplates selling everything and moving " + drugdisplay + " to sell drugs on a beach."

    bot.say(displaymsg)
