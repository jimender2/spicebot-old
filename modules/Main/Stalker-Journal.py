#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
from sopel import module, tools
import random
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('stalker')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    whotostalk = get_trigger_arg(bot, triggerargsarray, 1)
    if not whotostalk:
        
        botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
        blametargetarray = []
        for u in bot.users:
            if u in botusersarray and u != instigator and u != bot.nick:
                blametargetarray.append(u) 
        if blametargetarray == []:
            whotostalk = str(instigator + "'s mom")
        else:
            whotostalk = get_trigger_arg(bot, blametargetarray, 'random')
            bot.say("It's " + whotostalk + "'s fault.")
    elif whotostalk.lower() not in [u.lower() for u in bot.users]:
        bot.say("I'm not sure who that is.")
    else:
        bot.say("It's " + whotostalk + "'s fault.")
