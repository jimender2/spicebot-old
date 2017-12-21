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

validsubcommandarray = ['options','docs','help','warn','channel','modulecount','isowner','isop','isvoice','isadmin','on','off','isonforwho','timeout','usage']
GITWIKIURL = "https://github.com/deathbybandaid/sopel-modules/wiki"


@sopel.module.commands('spicebot')
def main_command(bot, trigger):
    ow = time.time()
    service = bot.nick.lower()
    maincommandused = trigger.group(1)
    triggerargsarray = create_args_array(trigger.group(2))
    subcommand = get_trigger_arg(triggerargsarray, 1)
    instigator = trigger.nick
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray, channel = special_users(bot)
    optedinarray, targetcantoptarray = [], []
    for u in allusersinroomarray:
        disenable = get_botdatabase_value(bot, u, 'disenable')
        if u != bot.nick and disenable:
            optedinarray.append(u)
        opttime = get_timesince(bot, u, 'opttime')
        if opttime < OPTTIMEOUT and not bot.nick.endswith(devbot):
            targetcantoptarray.append(u)
    inchannel = trigger.sender
    commandlist = get_trigger_arg(validsubcommandarray, "list")
    
    if not subcommand:
        bot.say("That's my name. Don't wear it out!")
    elif subcommand not in validsubcommandarray:
        bot.say("Invalid command. Options are: " + commandlist +".")
    
    ## Options
    elif subcommand == 'options':
        bot.say("Options are: " + commandlist +".")
        
    ## Docs
    elif subcommand == 'help' or subcommand == 'docs':
        bot.notice(instigator + ", Online Docs: " + GITWIKIURL, instigator)
        
    ## Warn against Bot abuse
    elif subcommand == 'warn' and inchannel.startswith("#"):
        target = get_trigger_arg(triggerargsarray, 2) or ''
        bot.msg(inchannel, target + "This is just a warning. Overuse of the bot, can get you kicked or banned by an operator. If you want to purely play with the bot, go to ##SpiceBot or ##SpiceBotTest, or send Spicebot a PrivateMessage.")
        
    ## Channel
    elif subcommand == 'channel':
        channelarray = []
        for c in bot.channels:
            channelarray.append(c)
        chanlist = get_trigger_arg(triggerargsarray, 'list')
        bot.say("You can find me in " + chanlist)
    
    ## Github Repo
    elif subcommand == 'github':
        bot.say('Spiceworks IRC Modules     https://github.com/deathbybandaid/sopel-modules')
    
    ## Modules
    elif subcommand == 'modulecount':
        modulecount = str(len(fnmatch.filter(os.listdir(moduledir), '*.py')))
        bot.say('There are currently ' + modulecount +' custom modules installed.')
        
    ## Bot Owner
    elif subcommand == 'isowner':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif target in botownerarray:
            bot.say(target + ' is the owner.')
        else:
            bot.say(target + ' is not the owner.')
    
    ## Bot Admin
    elif subcommand == 'isadmin':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif target in adminsarray:
            bot.say(target + ' is a bot admin.')
        else:
            bot.say(target + ' is not a bot admin.')
            
    ## Chan OP
    elif subcommand == 'isop':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif target in operatorarray:
            bot.say(target + ' is OP.')
        else:
            bot.say(target + ' is not OP.')
                        
    ## Chan VOICE
    elif subcommand == 'isvoice':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif target in voicearray:
            bot.say(target + ' is VOICE.')
        else:
            bot.say(target + ' is not VOICE.')
        
    ## On/off
    elif subcommand == 'on' or subcommand == 'off':
        disenablevalue = None
        if subcommand == 'on':
            disenablevalue = 1
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        targetopttime = get_timesince(bot, target, 'opttime')
        if target.lower() not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif target.lower() not in allusersinroomarray and target != 'everyone':
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif target != instigator and instigator not in adminsarray:
            bot.notice(instigator + "This is an admin only function.", instigator)
        elif target == 'everyone':
            for u in allusersinroomarray:
                set_botdatabase_value(bot, u, 'disenable', disenablevalue)
            bot.notice(instigator + ", " + bot.nick + " should now be " +  subcommand + ' for ' + target + '.', instigator)
        elif target in targetcantoptarray:
            bot.notice(instigator + " It looks like " + target + " can't enable/disable " + bot.nick + " for %d seconds." % (OPTTIMEOUT - targetopttime), instigator)
        elif subcommand == 'on' and target.lower() in optedinarray:
            bot.notice(instigator + ", It looks like " + target + " already has " + bot.nick + " on.", instigator)
        elif subcommand == 'off' and target.lower() not in optedinarray:
            bot.notice(instigator + ", It looks like " + target + " already has " + bot.nick + " off.", instigator)
        else:
            set_botdatabase_value(bot, target, 'disenable', disenablevalue)
            set_botdatabase_value(bot, target, 'opttime', now)
            bot.notice(instigator + ", " + bot.nick + " should now be " +  subcommand + ' for ' + target + '.', instigator)
    
    ## who is the bot on for
    elif subcommand == 'isonforwho' and inchannel.startswith("#"):
        bot.say('This command can only be run in privmsg.')
    elif subcommand == 'isonforwho' and not inchannel.startswith("#"):
        targetline = get_trigger_arg(optedinarray, "list") or ''
        chunks = targetarray.split()
        per_line = 15
        for i in range(0, len(chunks), per_line):
            targetline = " ".join(chunks[i:i + per_line])
            bot.say(str(targetline))
        if targetline == '':
            bot.say('Nobody has ' + bot.nick + " enabled.")
    
    ## usage
    elif subcommand == 'usage':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target.lower() not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        else:
            usertotal = get_botdatabase_value(bot, target, 'usertotal')
            bot.say(target + " has used " + str(usertotal) + " commands this hour.")
    
    ## timeout
    elif subcommand == 'timeout':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target.lower() not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        else:
            lasttime = get_timesince(bot, target, 'lastusagetime')
            if lasttime < LASTTIMEOUT:
                lasttimemath = int(LASTTIMEOUT - lasttime)
                message = str(target + " needs to wait " + str(lasttimemath) + " seconds to use Spicebot.")
            else:
                message = str(target + " should be able to use SpiceBot")
            bot.say(message)
    
    ## bot status
    elif subcommand == 'status':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target.lower() not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        else:
            disenable = get_botdatabase_value(bot, target, 'disenable')
            if disenable:
                message = str(target + " has SpiceBot enabled")
            else:
                message = str(target + " does not have SpiceBot enabled")
            bot.say(message)
    
    # can you see me
    elif subcommand == 'canyouseeme':
        bot.notice(instigator + ", I can see you.")
    
    
    
    
