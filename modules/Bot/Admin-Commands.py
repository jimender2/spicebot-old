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

@sopel.module.commands('spicebotadmin')
def main_command(bot, trigger):
    instigator = trigger.nick
    triggerargsarray = create_args_array(trigger.group(2))
    service = bot.nick.lower()
    subcommand = get_trigger_arg(triggerargsarray, 1)
    botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
    botchannel = trigger.sender
    channelarray = []
    for c in bot.channels:
        channelarray.append(c)
    
###### admin only block 
    if not trigger.admin:
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
            channelmodulesarray = get_botdatabase_value(bot, botchannel, 'channelmodules') or []
            if not commandtoenable:
                bot.say("What module do you want to "+str(dircommand)+"?")
            elif commandtoenable in channelmodulesarray and dircommand == 'enable':
                bot.say("It looks like this module is already enabled.")
            elif commandtoenable not in channelmodulesarray and dircommand == 'disable':
                bot.say("It looks like this module is already disabled.")
            else:
                if dircommand == 'enable':
                    adjust_database_array(bot, botchannel, commandtoenable, 'channelmodules', 'add')
                else:
                    adjust_database_array(bot, botchannel, commandtoenable, 'channelmodules', 'del')
                bot.say(commandtoenable + " should now be "+str(dircommand)+"d.")

    ## do a /me action for the bot in channel
    elif subcommand == 'chanaction' or subcommand == 'chanmsg':
        channel = get_trigger_arg(triggerargsarray, 2)
        message = get_trigger_arg(triggerargsarray, '3+')
        if not channel:
            bot.say("What channel?")
        elif channel not in channelarray:
            bot.say("Invalid channel.")
        elif not message:
            bot.say("What message?")
        elif subcommand == 'chanaction':
            bot.action(message,channel)
        elif subcommand == 'chanmsg':
            bot.msg(channel,message)
            
    ## Update from github
    elif subcommand == 'update':
        for channel in bot.channels:
            bot.msg(channel, trigger.nick + " commanded me to update from Github and restart. Be Back Soon!")
        update(bot, trigger)
        restart(bot, trigger, service)
    
    ## restart the bot's service
    elif subcommand == 'restart':
        for channel in bot.channels:
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
    
    
    
    
