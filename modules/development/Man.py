#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

GITWIKIURL = "https://github.com/deathbybandaid/SpiceBot/wiki"
custompagearray=['bot','usage'
                 'modules','commands',
                 'casino','gamble',
                 'challenge','duel',
                 'github',
                 'points',
                 'search',
                 'spicebucks',
                 'weather']

@sopel.module.commands('man')
def mainfunction(bot, trigger):
    triggerargsarray = create_args_array(trigger.group(2))
    subcommand = get_trigger_arg(triggerargsarray, 1)
    instigator = trigger.nick
    
    if subcommand in custompagearray:
        if subcommand == 'bot' or subcommand == 'usage':
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Using-the-Bot"
        if 'modules' or 'commands' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Modules"
        if duel or challenge in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Duels"
        if subcommand
        bot.say("There is a custom page for that. Find it here: " + str(CUSTOMPAGEURL))
    else:
        bot.say("Online Docs: " + GITWIKIURL)
