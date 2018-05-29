#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import re
import git
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

log_path = "data/templog.txt"
log_file_path = os.path.join(moduledir, log_path)

@sopel.module.commands('spicebotadmin')
def main_command(bot, trigger):
    instigator = trigger.nick
    inchannel = trigger.sender
    triggerargsarray = get_trigger_arg(bot, trigger.group(2), 'create')
    service = bot.nick.lower()
    subcommand = get_trigger_arg(bot, triggerargsarray, 1)
    botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
    botchannel = trigger.sender
    channelarray = []
    operatorarray = []
    for c in bot.channels:
        channelarray.append(c)
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray = special_users(bot)
    userarray = []
    for u in bot.users:
        userarray.append(u)
    
###### admin only block and OP
    if not trigger.admin and trigger.nick not in operatorarray:
        bot.notice(instigator + ", This is an admin/OP only function.", instigator)
    
    ## devmode
    elif subcommand == 'devmode':
        command = get_trigger_arg(bot, triggerargsarray, 2)
        if not command:
            osd_notice(bot, instigator, "Options are On or Off.")
            return
        if command == 'on':
            adjust_botdatabase_array(bot, bot.nick, [inchannel], 'devenabled', 'add')
            osd_notice(bot, instigator, "Devmode is on in " + inchannel + ".")
        else:
            adjust_botdatabase_array(bot, bot.nick, [inchannel], 'devenabled', 'del')
            osd_notice(bot, instigator, "Devmode is off in " + inchannel + ".")
    
    ## activate a module for a channel
    elif subcommand == 'chanmodules':
        channel = get_trigger_arg(bot, triggerargsarray, 2)
        dircommand = get_trigger_arg(bot, triggerargsarray, 3)
        validcommands = ['enable','disable','list']
        cmdarray = []
        for cmds in bot.command_groups.items():
            for cmd in cmds:
                if str(cmd).endswith("]"):
                    for x in cmd:
                        cmdarray.append(x)
        if not channel:
            bot.say('What Channel are we adjusting modules for?')
        elif channel not in channelarray:
            bot.say('Invalid channel.')
        elif not dircommand:
            bot.say("Would you like to enable/disable/list ?")
        elif dircommand not in validcommands:
            bot.say("A correct command is enable or disable.")
        elif dircommand == 'list':
            channelmodulesarray = get_botdatabase_value(bot, channel, 'channelmodules') or []
            validsubs = ['available','enabled','all']
            subscom = get_trigger_arg(bot, triggerargsarray, 4)
            if not subscom:
                bot.say('What list would you like? Options are all, available, enabled')
            elif subscom not in validsubs:
                bot.say('Invalid Option. Options are all, available, enabled')
            else:
                if subscom == 'all':
                    cmdlist = cmdarray
                elif subscom == 'enabled':
                    cmdlist = channelmodulesarray
                elif subscom == 'available':
                    availarray = []
                    for x in cmdarray:
                        if x not in channelmodulesarray:
                            availarray.append(x)
                    cmdlist = availarray
                cmdlist = get_trigger_arg(bot, cmdlist, 'list')
                chunks = cmdlist.split()
                per_line = 15
                cmdline = ''
                for i in range(0, len(chunks), per_line):
                    cmdline = " ".join(chunks[i:i + per_line])
                    bot.notice(str(cmdline), instigator)
        else:
            channelmodulesarray = get_botdatabase_value(bot, channel, 'channelmodules') or []
            commandtoenable = get_trigger_arg(bot, triggerargsarray, 4)
            if not commandtoenable:
                bot.say("What module do you want to "+str(dircommand)+" for " + channel + "?")
            elif commandtoenable == 'all':
                if dircommand == 'enable':
                    for x in cmdarray:
                        adjust_botdatabase_array(bot, channel, x, 'channelmodules', 'add')
                else:
                    adjust_botdatabase_array(bot, channel, x, 'channelmodules', None)
                bot.say("All Commands should now be "+str(dircommand)+"d for " + channel + ".")
            elif dircommand == 'enable' and commandtoenable not in cmdarray:
                bot.say("It looks like that is an invalid command to enable.")
            elif commandtoenable in channelmodulesarray and dircommand == 'enable':
                bot.say("It looks like the "+ commandtoenable +" module is already "+str(dircommand)+"d for " + channel + ".")
            elif commandtoenable not in channelmodulesarray and dircommand == 'disable':
                bot.say("It looks like the "+ commandtoenable +" module is already "+str(dircommand)+"d for " + channel + ".")
            else:
                if dircommand == 'enable':
                    adjust_botdatabase_array(bot, channel, commandtoenable, 'channelmodules', 'add')
                else:
                    adjust_botdatabase_array(bot, channel, commandtoenable, 'channelmodules', 'del')
                bot.say(commandtoenable + " should now be "+str(dircommand)+"d for " + channel + ".")

    ## do a /me action for the bot in channel
    elif subcommand == 'chanaction' or subcommand == 'chanmsg':
        channel = get_trigger_arg(bot, triggerargsarray, 2)
        message = get_trigger_arg(bot, triggerargsarray, '3+')
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
    
    ## Block users from using the bot
    elif subcommand == 'block' and not botchannel.startswith("#"):
        bot.say("blocks must be done in channel")
    elif subcommand == 'block':
        adddel = get_trigger_arg(bot, triggerargsarray, 2)
        target = get_trigger_arg(bot, triggerargsarray, 3)
        adddelarray = ['add','del']
        if not adddel:
            bot.say("would you like to add or del a user from the block list?")
        elif adddel not in adddelarray:
            bot.say("Invalid Command")
        elif not target:
            bot.say('Who do you want to block?')
        elif target not in userarray:
            bot.say("I don't know who that is.")
        else:
            if adddel == 'add':
                adjust_botdatabase_array(bot, botchannel, target, 'blockedusers', 'add')
                adddelword = "added to"
            else:
                adjust_botdatabase_array(bot, botchannel, target, 'blockedusers', 'del')
                adddelword = "removed from"
            bot.say(target + " has been " + adddelword + " the " + botchannel + " block list.")
    
    ## Block users from using the github module
    #elif subcommand == 'githubblock' and not botchannel.startswith("#"):
    #    bot.say("You must be in channel to block access to the github module.")
    elif subcommand == 'githubblock':
        adddel = get_trigger_arg(bot, triggerargsarray, 2)
        target = get_trigger_arg(bot, triggerargsarray, 3)
        adddelarray = ['add','del']
        if not adddel:
            bot.say("would you like to add or del a user from the github block list?")
        elif adddel not in adddelarray:
            bot.say("Invalid Command")
        elif not target:
            bot.say('Who do you want to block?')
        elif target not in userarray:
            bot.say("I don't know who that is.")
        else:
            if adddel == 'add':
                adjust_botdatabase_array(bot, bot.nick, target, 'githubblockedusers', 'add')
                adddelword = "added to"
            else:
                adjust_botdatabase_array(bot, bot.nick, target, 'githubblockedusers', 'del')
                adddelword = "removed from"
            bot.say(target + " has been " + adddelword + " the " + botchannel + " github block list.")
    
    ## On/off
    elif subcommand == 'on' or subcommand == 'off':
        disenablevalue = None
        if subcommand == 'on':
            disenablevalue = 1
        target = get_trigger_arg(bot, triggerargsarray, 2) or instigator 
        if target.lower() not in allusersinroomarray and target != 'everyone':
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif target == 'everyone':
            for u in allusersinroomarray:
                if disenablevalue == 1:
                    adjust_botdatabase_array(bot, bot.nick, u, 'botusers', 'add')
                else:
                    adjust_botdatabase_array(bot, bot.nick, u, 'botusers', 'del')
            bot.notice(instigator + ", " + bot.nick + " should now be " +  subcommand + ' for ' + target + '.', instigator)
        elif subcommand == 'on' and target.lower() in botusersarray:
            bot.notice(instigator + ", It looks like " + target + " already has " + bot.nick + " on.", instigator)
        elif subcommand == 'off' and target.lower() not in botusersarray:
            bot.notice(instigator + ", It looks like " + target + " already has " + bot.nick + " off.", instigator)
        else:
            if disenablevalue == 1:
                adjust_botdatabase_array(bot, bot.nick, target, 'botusers', 'add')
            else:
                adjust_botdatabase_array(bot, bot.nick, target, 'botusers', 'del')
            bot.notice(instigator + ", " + bot.nick + " should now be " +  subcommand + ' for ' + target + '.', instigator)
    
###### admin only block
    elif not trigger.admin:
        bot.notice(instigator + ", This is an admin only function.", instigator)
    
    ## Update from github
    elif subcommand == 'update':
        for channel in bot.channels:
            bot.msg(channel, trigger.nick + " commanded me to update from Github and restart. Be Back Soon!")
        update(bot, trigger)
        restart(bot, trigger, service)
    
    ## sometimes Update from github doesn't work because of file permissions
    elif subcommand == 'permfix':
        os.system("sudo chown -R spicebot:sudo /home/spicebot/.sopel/")
        bot.say("Permissions should now be fixed")
    
    ## restart the bot's service
    elif subcommand == 'restart':
        for channel in bot.channels:
            bot.msg(channel, trigger.nick + " Commanded me to restart. Be Back Soon!")
        restart(bot, trigger, service)   
                
    ## install a python pip package
    elif subcommand == 'pipinstall':
        pippackage = get_trigger_arg(bot, triggerargsarray, '2+')
        if not pippackage:
            bot.say("You must specify a pip package")
        else:
            bot.say("attempting to install " + pippackage)
            os.system("sudo pip install " + pippackage)
            bot.say('Possibly done installing ' + pippackage)      
               
    ## Check the latest logs from the last time logs were checked or cleared
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
                if search_phrase in str(line):
                    mostrecentstartbot = line_num
            line_num = 0
        with open(log_file_path) as fb:
            for line in fb:
                line_num += 1
                currentline = line_num
                if int(currentline) >= int(mostrecentstartbot) and not any(x in line for x in ignorearray):
                    bot.say(str(line))
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
    
