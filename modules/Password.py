#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('password')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    password = get_trigger_arg(triggerargsarray, 0)
    if not password:
        bot.say("If you type your password here, I will obscure it.")
    else:
        amountofletters = len(password)
        mystring = "*" * amountofletters
        bot.say("Your password is: " + str(mystring))
