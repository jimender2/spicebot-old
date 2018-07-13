#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib2
import json
from BeautifulSoup import BeautifulSoup
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

#author jimender2

@sopel.module.commands('misty')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):

    instigator = trigger.nick
    inputstring = get_trigger_arg(bot, triggerargsarray, '1+')
    if not inputstring:
        inputstring = "biznatch"
    bot.say("%s thinks it's starting to get a little misty up in %s" %(instigator, inputstring))
