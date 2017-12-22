#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *
#from shareddir.path.append(Main) import Nuke ##this line is wonky


@sopel.module.commands('testimport')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
  
def execute_main(bot, trigger, triggerargsarray):
    ## Initial ARGS
    triggerargsarray = create_args_array(trigger.group(2)) ## triggerarg 0 = commandused
    subcommandused = get_trigger_arg(triggerargsarray, 1)
     
    if subcommandused == 'nuke':
        nukeit(bot, trigger, triggerargsarray)
    else:
      bot.say('Module error')
