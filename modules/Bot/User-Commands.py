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

GITWIKIURL = "https://github.com/deathbybandaid/SpiceBot/wiki"

@sopel.module.commands('spicebot')
def main_command(bot, trigger):
    triggerargsarray = create_args_array(trigger.group(2))
    subcommand = get_trigger_arg(triggerargsarray, 1)
    instigator = trigger.nick
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray = special_users(bot)
    botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
    inchannel = trigger.sender
    
    if not subcommand:
        bot.say("That's my name. Don't wear it out!")
        
    ## Docs
    elif subcommand == 'help' or subcommand == 'docs':
        bot.notice(instigator + ", Online Docs: " + GITWIKIURL, instigator)
        
    ## Warn against Bot abuse
    elif subcommand == 'warn' and inchannel.startswith("#"):
        target = get_trigger_arg(triggerargsarray, 2) or ''
        bot.msg(inchannel, target + "This is just a warning. Overuse of the bot, can get you kicked or banned by an operator. If you want to purely play with the bot, go to ##SpiceBot or ##SpiceBotTest, or send Spicebot a PrivateMessage.")

    ## Github Repo
    elif subcommand == 'github':
        bot.say('Spiceworks IRC Modules     https://github.com/deathbybandaid/SpiceBot')
    
    ## Modules
    elif subcommand == 'modulecount':
        modulecount = str(len(fnmatch.filter(os.listdir(moduledir), '*.py')))
        bot.say('There are currently ' + modulecount +' custom modules installed.')
        
    ## Bot Owner
    elif subcommand == 'owner':
        ownerlist = get_trigger_arg(botownerarray, 'list')
        bot.notice("Bot Owners are: " + ownerlist, instigator)
    
    ## Bot Admin
    elif subcommand == 'admin':
        adminlist = get_trigger_arg(adminsarray, 'list')
        bot.notice("Bot Admin are: " + adminlist, instigator)
        
    ## usage
    elif subcommand == 'usage':
        bot.say("Work In Progress")
    
    ## can you see me
    elif subcommand == 'canyouseeme':
        bot.notice(instigator + ", I can see you.")
        
    ## On/off
    elif subcommand == 'on' or subcommand == 'off':
        if subcommand == 'on' and instigator in botusersarray:
            bot.notice(instigator + ", It looks like you already have " + bot.nick + " on.", instigator)
        elif subcommand == 'off' and instigator not in botusersarray:
            bot.notice(instigator + ", It looks like you already have " + bot.nick + " off.", instigator)
        else:
            if subcommand == 'on':
                adjust_database_array(bot, bot.nick, instigator, 'botusers', 'add')
            else:
                adjust_database_array(bot, bot.nick, instigator, 'botusers', 'del')
            bot.notice(instigator + ", " + bot.nick + " should now be " +  subcommand + ' for ' + instigator + '.', instigator)
