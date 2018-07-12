#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('nuke','killit','terminate')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'nuke')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    commandused = trigger.group(1)
    target = get_trigger_arg(bot, triggerargsarray, '1+') or 'notarget' ## triggerargsarray 0 is the command itself
    if commandused == 'nuke':
        nukeit(bot, trigger, triggerargsarray)
    elif commandused == 'killit':
        killitnow(bot, trigger, triggerargsarray)
    elif commandused == 'terminate':
        terminateit(bot, trigger, triggerargsarray, target)

def nukeit(bot, trigger, triggerargsarray):
    bot.say("Nuke it from orbit... it's the only way to be sure?")
    
def killitnow(bot, trigger, triggerargsarray):
    bot.say("Kill it with fire. Now.")

def terminateit(bot, trigger, triggerargsarray, target):
    if target == 'notarget':
        bot.say("Terminate it with extreme prejudice.")
    elif target:
        bot.action("terminates "+ target +" with extreme prejudice.")
