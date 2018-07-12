#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
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
    validtarget= targetcheck(bot,target,trigger.nick)
    channel = trigger.sender
    if not target:
        bot.say("Who is supersoft?")
    elif target == instigator:
        bot.say('Is your self esteem really that low?')
    elif validtarget==0:
        bot.say("I'm not sure who that is.")
    elif validtarget == 2:
        bot.say("I'm all metal, baby")
    else:
        pick=random.randint(1,20)
        if pick ==1:
            bot.say(target + " is going to have a super soft birthday party this year.")
        else:
            bot.say(target + " is supersoft. 10-ply. Now give your balls a tug, tit-fucker and figger it out. Ferda!")
