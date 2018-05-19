#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

weapontypes = ["Axe","Sword","Revolver"]
adjectives = ["big", "small", "tiny", "huge", "bloody", "shiny"]

@sopel.module.commands('murder','moida')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'murder')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick


#start of test code
x = 0
u = 0
    allchanweaponsarray = []
    for u in bot.users:
        weaponslist = get_database_value(bot, u, 'weaponslocker_complete') #or ['fist']
        for x in weaponslist:
            allchanweaponsarray.append(x)
    weapontype = get_trigger_arg(bot, allchanweaponsarray, 'random')
#end of test code


    target = get_trigger_arg(bot, triggerargsarray, 1)
    reason = get_trigger_arg(bot, triggerargsarray, '2+')
    message = "Whoops, something went wrong."
#    weapontype = get_trigger_arg(bot,weapontypes,'random')
    adjective = get_trigger_arg(bot,adjectives,'random')
    msg = "a " + adjective + " " + weapontype

    # No target specified
    if not target:
        bot.say("Who/what would you like to murder?")

    # Cannot kill spicebot
    elif target == bot.nick:
        bot.say("You cannot kill a nonliving entity")

    # Cannot kill self
    elif target == instigator:
		message = "Killing yourself would be suicide, " + instigator + ", not murder. Idiot."
		bot.say(message)

    # Target is fine
    else:
        if not reason:
            message = instigator + " murders " + target + " with " + msg + "."
        else:
            message = instigator + " murders " + target + " with " + msg + " for " + reason + "."
        bot.say(message)

#
#
#
#
#TEST CODE
def get_database_value(bot, nick, databasekey):
    databasecolumn = str('duels_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value