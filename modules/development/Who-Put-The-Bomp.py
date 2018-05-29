#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
#import sopel.module
from sopel.module import commands, nickname_commands, rule, priority, example
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@nickname_commands('who put the')
#@sopel.module.commands('who')
@commands('who')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    funlist = ["Who put the bomp in the bomp bah bomp bah bomp","Who put the ram in the rama lama ding dong","Who put the bop in the bop shoo bop shoo bop","Who put the dip in the dip da dip da dip"]
    answer = get_trigger_arg(bot, funlist, 'random')
    bot.say(answer)
