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
sys.path.append(moduledir)
from SpicebotShared import *

OPTTIMEOUT = 1800
FINGERTIMEOUT = 1800
TOOMANYTIMES = 15
LASTTIMEOUT = 60
LASTTIMEOUTHOUR = 3600

GITWIKIURL = "https://github.com/deathbybandaid/sopel-modules/wiki"

validsubcommandarray = ['options','docs','help','warn,'channel','modulecount','isowner']

@sopel.module.commands('spicebot','spicebotadmin')
def main_command(bot, trigger):
    now = time.time()
    maincommandused = trigger.group(1)
    subcommand = get_trigger_arg(triggerargsarray, 2)
    instigator = trigger.nick
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray, channel = special_users(bot)
    inchannel = trigger.sender
    commandlist = get_trigger_arg(validsubcommandarray, "list")
    if not subcommand:
        bot.say("That's my name. Don't wear it out!")
    elif subcommand not in validsubcommandarray or subcommand == 'options':
        bot.say("Invalid command. Options are: " + commandlist +".")
    
    ## Docs
    elif subcommand == 'help' or subcommand == 'docs':
        bot.notice(instigator + ", Online Docs: " + GITWIKIURL, instigator)
        
    ## Warn against Bot abuse
    elif subcommand == 'warn':
        target = get_trigger_arg(triggerargsarray, 3) or ''
        bot.msg(channel, target + "This is just a warning. Overuse of the bot, can get you kicked or banned by an operator. If you want to purely play with the bot, go to ##SpiceBotTest, or send Spicebot a PrivateMessage.")
        
    ## Channel
    elif subcommand == 'channel':
        bot.say("You can find me in " + channel)
    
    ## Modules
    elif subcommand == 'modulecount':
        modulecount = str(len(fnmatch.filter(os.listdir(moduledir), '*.py')))
        bot.say('There are currently ' + modulecount +' custom modules installed.')
        
    ## Bot Owner
    elif subcommand == 'isowner':
        target = get_trigger_arg(triggerargsarray, 3) or instigator
        if target not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            
        
        
    ##
    
    ##
    
    ##
    
    ##
        
    
