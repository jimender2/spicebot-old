#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

weapontypes = ["Axe","example"]

@sopel.module.commands('murder')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    target = get_trigger_arg(bot, triggerargsarray, 1)
    reason = get_trigger_arg(bot, triggerargsarray, '2+')
    message = "Whoops, something went wrong."
    weapontype = get_trigger_arg(bot,weapontypes,'random')
    msg = "a " + weapontype
    
    # No target specified
    if not target:
        bot.say("Who/what would you like to murder?")
    
    # Can slap the bot
    if target == bot.nick:
        message = trigger.nick + " slaps " + target + " with " + msg + " for " + reason + "."
        bot.say(message)
        bot.say("That hurts")
        
    # Target is fine
    else:
        if not reason:
            message = trigger.nick + " slaps " + target + " with " + msg + "."
        else:
            if reason.startswith('for ') or reason.startswith('because ') or reason.startswith('cause '):
                message = trigger.nick + " slaps " + target + " with " + msg + " " + reason + "."
            else:
                message = trigger.nick + " slaps " + target + " with " + msg + " for " + reason + "."
        bot.say(message)
