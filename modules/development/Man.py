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
                 'challenge','challenges','duel','duels',
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
        if subcommand == 'bot' or subcommand == 'usage':
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Using-the-Bot"
        if 'module' or 'command' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Modules"
        if 'duel' or 'challenge' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Duels"
        if subcommand == 'github':
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Github"
        if subcommand == 'pants' or subcommand == 'points':
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Points"
        if 'search' or 'google' or 'lookup' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Search"
        if 'spicebuck' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Duels"
        if subcommand == 'weather':
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Weather"
        bot.say("There is a custom page for that. Find it here: " + str(CUSTOMPAGEURL))
    else:
        bot.say("Online Docs: " + GITWIKIURL)
