#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('supersoft')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    target = get_trigger_arg(bot, triggerargsarray, 1)
    channel = trigger.sender
    if not target:
        bot.say("Who is supersoft?")
    elif target == instigator:
        bot.say('Is your self esteem really that low?')
    elif not targetcheck(bot,target,trigger.nick)==1:
        bot.say("I'm not sure who that is.")
    elif target == 2
        bot.say("I am all metal")
    else:
        message = target + " is going to have a super soft birthday party this year."
        onscreentext(bot,msg,channel)
