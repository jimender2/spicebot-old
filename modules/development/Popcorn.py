#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

#author jimender2

weapontypes = ["Axe","Sword","Revolver"]
commandarray = ["add","remove","count","last"]

@sopel.module.commands('popcorn','pc')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'popcorn')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    bot.action("munch, munch")
    bot.say("https://media2.giphy.com/media/daJWXqaZFqh0s/giphy.gif")