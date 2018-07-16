#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from random import random
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

@sopel.module.commands('sexbot','cockbot','fuckbot')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)

def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    rando = randint(2, 22)
    bot.say("Please insert " + str(rando) + " bitcoins, for that kind of service.")
