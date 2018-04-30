#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('dd','doubled','DoubleD')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'dd')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    target = get_trigger_arg(bot, triggerargsarray, 1)
    if not target:
        bot.say("Who are you pissed at now?")
    elif target.lower() not in [u.lower() for u in bot.users]:
        bot.say("I'm not sure who that is.")
    elif target == bot.nick:
        bot.say("Ummm, no. Dumbass.")
    else:
        bot.action('punches ' + target + ', who is clearly a motherfucker, in the mouth.')
