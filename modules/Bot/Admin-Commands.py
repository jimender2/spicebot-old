#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel import module, tools
from sopel.module import ADMIN
from sopel.module import VOICE
from sopel.module import event, rule
from sopel.module import OP
from sopel.tools.target import User, Channel
import time
import os
import sys
import fnmatch
import re
import git 
from os.path import exists
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

log_path = "data/templog.txt"
log_file_path = os.path.join(moduledir, log_path)

devbot = 'dev' ## If using a development bot and want to bypass commands, this is what the bots name ends in

OPTTIMEOUT = 1800
FINGERTIMEOUT = 1800
TOOMANYTIMES = 7
LASTTIMEOUT = 30

GITWIKIURL = "https://github.com/deathbybandaid/sopel-modules/wiki"

validsubcommandarray = ['options','docs','help','warn','channel','modulecount','isowner','isop','isvoice','isadmin','on','off','isonforwho','timeout','usage']

statsadminchangearray = ['hourwarned','usertotal','lastopttime']

@sopel.module.commands('spicebotadmin')
def main_command(bot, trigger):
    now = time.time()
    service = bot.nick.lower()
    maincommandused = trigger.group(1)
    triggerargsarray = create_args_array(trigger.group(2))
    subcommand = get_trigger_arg(triggerargsarray, 1)
    instigator = trigger.nick
    triggerargsarray = create_args_array(trigger.group(2))
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray, channel = special_users(bot)
    botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
    inchannel = trigger.sender
    commandlist = get_trigger_arg(validsubcommandarray, "list")
    botchannel = trigger.sender
    
###### admin only block 
    if instigator not in adminsarray:
        bot.notice(instigator + "This is an admin only function.", instigator)
    
    ## activate a module for a channel
    elif subcommand == 'chanmodules' and botchannel.startswith("#"):
        dircommand = get_trigger_arg(triggerargsarray, 2)
        validcommands = ['enable','disable']
        if not dircommand:
            bot.say("Would you like to enable or disable a module?")
        elif dircommand not in validcommands:
            bot.say("A correct command is enable or disable.")
        else:
            commandtoenable = get_trigger_arg(triggerargsarray, 3)
            if not commandtoenable:
                bot.say("What module do you want to enable?")
            elif dircommand == 'enable':
                adjust_database_array(bot, botchannel, commandtoenable, 'channelmodules', 'add')
            else:
                adjust_database_array(bot, botchannel, commandtoenable, 'channelmodules', 'del')

    ## do a /me action for the bot in channel
    elif subcommand == 'chanaction':
        message = get_trigger_arg(triggerargsarray, '2+')
        if message:
            bot.action(message,channel)
    
    ## Make the bot talk in channel
    elif subcommand == 'chanmsg':
        message = get_trigger_arg(triggerargsarray, '2+')
        if message:
            bot.msg(channel,message)
    
    ## set and reset values
    elif subcommand == 'statsadmin':
        incorrectdisplay = "A correct command use is .spicebotadmin statsadmin target set/reset stat"
        target = get_trigger_arg(triggerargsarray, 2)
        subcommand = get_trigger_arg(triggerargsarray, 3)
        statset = get_trigger_arg(triggerargsarray, 4)
        newvalue = get_trigger_arg(triggerargsarray, 5) or None
        if not target:
            bot.notice(instigator + ", Target Missing. " + incorrectdisplay, instigator)
        elif target.lower() not in allusersinroomarray and target != 'everyone':
            bot.notice(instigator + ", It looks like " + str(target) + " is either not here, or not a valid person.", instigator)
        elif not subcommand:
            bot.notice(instigator + ", Subcommand Missing. " + incorrectdisplay, instigator)
        elif subcommand not in statsadminchangearray:
            bot.notice(instigator + ", Invalid subcommand. " + incorrectdisplay, instigator)
        elif not statset:
            bot.notice(instigator + ", Stat Missing. " + incorrectdisplay, instigator)
        elif statset not in statsadminarray and statset != 'all':
            bot.notice(instigator + ", Invalid stat. " + incorrectdisplay, instigator)
        elif instigator not in adminsarray:
            bot.notice(instigator + "This is an admin only function.", instigator)
        else:
            if subcommand == 'reset':
                newvalue = None
            if subcommand == 'set' and newvalue == None:
                bot.notice(instigator + ", When using set, you must specify a value. " + incorrectdisplay, instigator)
            elif target == 'everyone':
                for u in bot.channels[channel].users:
                    if statset == 'all':
                        for x in statsadminarray:
                            set_botdatabase_value(bot, u, x, newvalue)
                    else:
                        set_botdatabase_value(bot, u, statset, newvalue)
                bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)
            else:
                if statset == 'all':
                    for x in statsadminarray:
                        set_botdatabase_value(bot, target, x, newvalue)
                else:
                    set_botdatabase_value(bot, target, statset, newvalue)
                bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)

    ## Update from github
    elif subcommand == 'update':
        bot.msg(channel, trigger.nick + " commanded me to update from Github and restart. Be Back Soon!")
        update(bot, trigger)
        restart(bot, trigger, service)
    
    ## restart the bot's service
    elif subcommand == 'restart':
        bot.msg(channel, trigger.nick + " Commanded me to restart. Be Back Soon!")
        restart(bot, trigger, service)   
                
    ## install a python pip package
    elif subcommand == 'pipinstall':
        pippackage = get_trigger_arg(triggerargsarray, '2+')
        if not pippackage:
            bot.say("You must specify a pip package")
        else:
            bot.say("attempting to install " + pippackage)
            os.system("sudo pip install " + pippackage)
            bot.say('Possibly done installing ' + pippackage)      
                
    elif subcommand == 'debug':
        debugloglinenumberarray = []
        bot.action('Is Copying Log')
        os.system("sudo journalctl -u " + service + " >> " + log_file_path)
        bot.action('Is Filtering Log')
        search_phrase = "Welcome to Sopel. Loading modules..."
        ignorearray = ['session closed for user root','COMMAND=/bin/journalctl','COMMAND=/bin/rm','pam_unix(sudo:session): session opened for user root']
        mostrecentstartbot = 0
        with open(log_file_path) as f:
            line_num = 0
            for line in f:
                line_num += 1
                if search_phrase in line:
                    mostrecentstartbot = line_num
            line_num = 0
        with open(log_file_path) as fb:
            for line in fb:
                line_num += 1
                currentline = line_num
                if int(currentline) >= int(mostrecentstartbot) and not any(x in line for x in ignorearray):
                    bot.say(line)
        bot.action('Is Removing Log')
        os.system("sudo rm " + log_file_path)

def restart(bot, trigger, service):
    bot.say('Restarting Service...')
    os.system("sudo service " + str(service) + " restart")
    bot.say('If you see this, the service is hanging. Making another attempt.')

def update(bot, trigger):
    bot.say('Pulling From Github...')
    g = git.cmd.Git(moduledir)
    g.pull()
    
    
    
    
