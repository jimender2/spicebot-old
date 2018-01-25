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
custompagearray=['bot','usage','spicebot',
                 'module','modules','command','commands',
                 'casino','gamble','gambling',
                 'challenge','challenges','duel','duels','dueling','duelling',
                 'github',
                 'man',
                 'pants','points',
                 'search','searching','google','lookup',
                 'spicebucks','spicebuck',
                 'weather']
custompages=['spicebot','modules','casino','duel','github','man','pants','points','search','spicebucks','weather']


@sopel.module.commands('man')
def mainfunction(bot, trigger):
    triggerargsarray = create_args_array(trigger.group(2))
    subcommand = get_trigger_arg(triggerargsarray, 1)
    customdisplay =  get_trigger_arg(canduelarray, "list")
    if subcommand == 'options' or subcommand == 'help':
        bot.say("Modules with custom pages include: " + customdisplay)
    if subcommand in custompagearray:
        if 'bot' in subcommand or 'usage' in subcommand or 'spicebot' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Using-the-Bot"
        elif 'module' in subcommand or 'command' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Modules"
        elif 'duel' in subcommand or 'challenge' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Duels"
        elif 'github' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Github"
        elif 'man' in subcommand or 'help' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Man"
        elif 'pants' in subcommand or 'points' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Points"
        elif 'search' in subcommand or 'google'in subcommand  or 'lookup' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Search"
        elif 'spicebuck' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Spicebucks"
        elif 'weather' in subcommand:
            CUSTOMPAGEURL = str(GITWIKIURL)+"/Weather"
        bot.say("There is a custom page for that. Find it here: " + str(CUSTOMPAGEURL))
    else:
        bot.say("The guide for the bot can be found here: " + GITWIKIURL)
