#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import urllib
import sys
import os
from word2number import w2n
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

fra='https://raw.githubusercontent.com/deathbybandaid/SpiceBot/master/Text-Files/ferengi_rules.txt'

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
        requested.lstrip("-")        
        if (requested == '0' or requested.lower() == 'zero'):
            myline = randomfra()
        else:
            htmlfile=urllib.urlopen(fra)
            lines=htmlfile.readlines()
            if (requested == '0' or requested.lower() == 'zero'):
                myline = randomfra()
            else:
                if requested.isdigit():
                    rulenumber = int(requested)
                    myline = get_trigger_arg(lines, rulenumber)
                else:
                    try:
                        rulenumber = w2n.word_to_num(str(requested))
                        myline = get_trigger_arg(lines, rulenumber)   
                    except ValueError:
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
