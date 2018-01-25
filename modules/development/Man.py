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
                 'module','modules','command','commands',
                 'casino','gamble','gambling',
                 'challenge','challenges','duel','duels','dueling','duelling',
                 'github',
                 'pants','points',
                 'search','searching','google','lookup',
                 'spicebuck','spicebuck',
                 'weather']

@sopel.module.commands('man')
def mainfunction(bot, trigger):
    triggerargsarray = create_args_array(trigger.group(2))
    subcommand = get_trigger_arg(triggerargsarray, 1)
    instigator = trigger.nick
    
    if subcommand in custompagearray:
        if 'bot' or 'usage' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Using-the-Bot"
        elif 'module' or 'command' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Modules"
        elif 'duel' or 'challenge' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Duels"
        elif 'github' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Github"
        elif 'pants' or 'points' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Points"
        elif 'search' or 'google' or 'lookup' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Search"
        elif 'spicebuck' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Spicebucks"
        elif 'weather' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Weather"
        bot.say("There is a custom page for that. Find it here: " + str(CUSTOMPAGEURL))
    else:
        bot.say("Online Docs: " + GITWIKIURL)
