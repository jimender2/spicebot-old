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

@sopel.module.commands('poop','poops')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    failureodds =4
    if bot.nick.endswith('dev'):
        failureodds = 2
    backfires= [" drops their pants and squats on targets desk, but all they manage to do is fart.", 
                " overestimated their capabilities and poops themselves.",  
                " halfway through pooping on the desk before realising that they are pooping on their own desk.", 
                " trips over taking their pants off and shits everywhere BUT the desk."]

    target = get_trigger_arg(triggerargsarray, 1)
    if not target:
        bot.say(trigger.nick + ' poops in the designated corner!')
    elif target == 'group':
        bot.say(trigger.nick + ', get your poop in a group.')
    elif target == 'all' or target == 'everyone' or target == 'everyones':
        bot.say(trigger.nick + " poops on everyone's desk, one at a time!")
    elif target != bot.nick:        
        failchance = random.randint(1,failureodds)
        if failchance == 1:
            poopfail = get_trigger_arg(backfires,'random')            
            bot.say(trigger.nick + poopfail)
        else:
            bot.say(trigger.nick + ' poops on ' + target + "'s desk, maintaining eye contact the entire time!")
