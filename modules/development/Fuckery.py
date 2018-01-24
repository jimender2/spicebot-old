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
    duelusersarray = get_database_value(bot, bot.nick, 'duelusers') or []
    inchannel = trigger.sender
    
    if not subcommand:
        bot.say("Do you want fuckery on or off?")
    if subcommand == 'enable' or subcommand == 'commence':
        subcommand = 'on'
    if subcommand == 'disable' or subcommand == 'quit':
        subcommand = 'off'
        
    ## On/off
    if subcommand == 'on' or subcommand == 'off':
        if subcommand == 'on':
            if instigator not in botusersarray:
                adjust_database_array(bot, bot.nick, instigator, 'botusers', 'add')
            if instigator not in duelusersarray:
                adjust_db_array(bot, bot.nick, instigator, 'duelusers', 'add')
            bot.say(instigator + " has now opted in to every optional module. Let the fuckery commence!")
        else:
            if instigator in botusersarray:
                adjust_database_array(bot, bot.nick, instigator, 'botusers', 'del')
            if instigator in duelusersarray:
                adjust_db_array(bot, bot.nick, instigator, 'duelusers', 'del')
            bot.say(instigator + " has opted out of using the bot. Quitter.")

## duel database functions
def get_database_value(bot, nick, databasekey):
    databasecolumn = str('duels_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
return database_value

def adjust_db_array(bot, nick, entry, databasekey, adjustmentdirection):
    adjustarray = get_database_value(bot, nick, databasekey) or []
    adjustarraynew = []
    for x in adjustarray:
        adjustarraynew.append(x)
    set_database_value(bot, nick, databasekey, None)
    adjustarray = []
    if adjustmentdirection == 'add':
        if entry not in adjustarraynew:
            adjustarraynew.append(entry)
    elif adjustmentdirection == 'del':
        if entry in adjustarraynew:
            adjustarraynew.remove(entry)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        set_database_value(bot, nick, databasekey, None)
    else:
set_database_value(bot, nick, databasekey, adjustarray)
