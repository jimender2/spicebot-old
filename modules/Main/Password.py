#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('password')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    password = get_trigger_arg(bot, triggerargsarray, 0)
    if not password:
        bot.say("If you type your password here, I will obscure it.")
    else:
        amountofletters = len(password)
        mystring = "*" * amountofletters
        bot.say("Your password is: " + str(mystring))
