#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

weapontypes = ["Axe","Sword","Revolver"]

@sopel.module.commands('murder','moida')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'murder')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    target = get_trigger_arg(bot, triggerargsarray, 1)
    reason = get_trigger_arg(bot, triggerargsarray, '2+')
    message = "Whoops, something went wrong."
    weapontype = get_trigger_arg(bot,weapontypes,'random')
    msg = "a " + weapontype

    # No target specified
    if not target:
        bot.say("Who/what would you like to murder?")

    # Cannot kill spicebot
    if target == bot.nick:
		if not reason:
			message = instigator + " attempts to murder " + target + " with " + msg + "."
		else:
			message = instigator + " attempts to murder " + target + " with " + msg + " for " + reason + "."
		bot.say(message)
		bot.say("You cannot kill a nonliving entity")

    # Cannot kill self
	if target == instigator:
		message = instigator + " cannot murder themselves. That would be suicide."
		bot.say(message)

	# Target is fine
	else:
		if not reason:
			message = instigator + " murders " + target + " with " + msg + "."
        else:
			message = instigator + " murders " + target + " with " + msg + " for " + reason + "."	
		bot.say(message)
