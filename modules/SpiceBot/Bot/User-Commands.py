#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

GITWIKIURL = "https://github.com/deathbybandaid/SpiceBot/wiki"

@sopel.module.commands('spicebot')
def main_command(bot, trigger):
    triggerargsarray = get_trigger_arg(bot, trigger.group(2), 'create')
    subcommand = get_trigger_arg(bot, triggerargsarray, 1)
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
        target = get_trigger_arg(bot, triggerargsarray, 2) or ''
        bot.msg(inchannel, target + "This is just a warning. Overuse of the bot, can get you kicked or banned by an operator. If you want to purely play with the bot, go to ##SpiceBot or ##SpiceBotTest, or send Spicebot a PrivateMessage.")

    ## Github Repo
    elif subcommand == 'github':
        bot.say('Spiceworks IRC Modules     https://github.com/deathbybandaid/SpiceBot')

    ## gender
    elif subcommand == 'gender':
        bot.say("Female.")
    ## Modules
    elif subcommand == 'modulecount':
        cmdarray = []
        for cmds in bot.command_groups.items():
            for cmd in cmds:
                if str(cmd).endswith("]"):
                    for x in cmd:
                        cmdarray.append(x)
        bot.say('There are currently ' + str(len(cmdarray)) +' custom modules installed.')

    ## Bot Owner
    elif subcommand == 'owner':
        ownerlist = get_trigger_arg(bot, botownerarray, 'list')
        bot.notice("Bot Owners are: " + ownerlist, instigator)

    ## Bot Admin
    elif subcommand == 'admin':
        adminlist = get_trigger_arg(bot, adminsarray, 'list')
        bot.notice("Bot Admin are: " + adminlist, instigator)

    ## usage
    elif subcommand == 'usage':
        bot.say("Work In Progress")

    ## can you see me
    elif subcommand == 'canyouseeme':
        bot.notice(instigator + ", I can see you.")

    ## Is the bot on?
    elif subcommand == 'status':
        target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
        if target.lower() not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        else:
            if target in botusersarray:
                message = str(target + " has SpiceBot enabled")
            else:
                message = str(target + " does not have SpiceBot enabled")
            bot.say(message)

    ## On/off
    elif subcommand == 'on' or subcommand == 'off':
        if subcommand == 'on' and instigator in botusersarray:
            bot.notice(instigator + ", It looks like you already have " + bot.nick + " on.", instigator)
        elif subcommand == 'off' and instigator not in botusersarray:
            bot.notice(instigator + ", It looks like you already have " + bot.nick + " off.", instigator)
        else:
            if subcommand == 'on':
                adjust_botdatabase_array(bot, bot.nick, instigator, 'botusers', 'add')
            else:
                adjust_botdatabase_array(bot, bot.nick, instigator, 'botusers', 'del')
            bot.notice(instigator + ", " + bot.nick + " should now be " +  subcommand + ' for ' + instigator + '.', instigator)
