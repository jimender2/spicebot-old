#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('lazy','lazyfuckingspicebot','fuckinglazyspicebot','lazyspicebot')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    target=get_trigger_arg(bot,triggerargsarray,1)
    validtarget = targetcheck(bot,target,trigger.nick)
    if validtarget=='1':
        bot.say('I do not tell you how to do your job, %s!!' % target) 
    else:
        bot.say('I do not tell you how to do your job, %s!!' % trigger.nick)
