#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

### opt-in modules - spicebot, duels

@sopel.module.commands('fuckery')
def main_command(bot, trigger):
    triggerargsarray = create_args_array(trigger.group(2))
    subcommand = get_trigger_arg(triggerargsarray, 1)
    instigator = trigger.nick
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray = special_users(bot)
    botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
    inchannel = trigger.sender
    
    if not subcommand:
        bot.say("Do you want fuckery on or off?")
    if subcommand == 'enable' or subcommand == 'commence':
        subcommand = 'on'
    if subcommand == 'disable' or subcommand == 'quit':
        subcommand = 'off'
        
    ## On/off
    if subcommand == 'on' or subcommand == 'off':
        if subcommand == 'on' and instigator in botusersarray:
            bot.notice(instigator + ", It looks like you already have " + bot.nick + " on.", instigator)
        elif subcommand == 'off' and instigator not in botusersarray:
            bot.notice(instigator + ", It looks like you already have " + bot.nick + " off.", instigator)
        else:
            if subcommand == 'on':
                adjust_database_array(bot, bot.nick, instigator, 'botusers', 'add')
                adjust_database_array(bot, bot.nick, target, 'duelusers', 'add')
            else:
                adjust_database_array(bot, bot.nick, instigator, 'botusers', 'del')
                adjust_database_array(bot, bot.nick, target, 'duelusers', 'del')
bot.notice(instigator + ", " + bot.nick + "and Duels should now be " + subcommand + ' for ' + instigator + '.', instigator)
