#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import urllib
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

fra='https://raw.githubusercontent.com/deathbybandaid/sopel-modules/dev/otherfiles/ferengi_rules.txt'

@sopel.module.commands('ferengi')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    requested = get_trigger_arg(triggerargsarray, 0)
    if not requested:
        myline = randomfra()
    else:
        rulenumber = int(requested)
        htmlfile=urllib.urlopen(fra)
        lines=htmlfile.readlines()
        try:
            myline = str(lines[rulenumber-1])
        except IndexError:
            myline = 'That doesnt appear to be a rule number.'
        if not myline or myline == '\n':
            myline = 'There is no cannonized rule tied to this number.'
    bot.say(myline)
       
# random rule
def randomfra():
    htmlfile=urllib.urlopen(fra)
    lines=htmlfile.read().splitlines()
    myline=random.choice(lines)
    if not myline or myline == '\n':
        myline = randomfra()
    return myline
