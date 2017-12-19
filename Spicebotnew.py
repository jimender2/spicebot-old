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

@sopel.module.commands('spicebot','spicebotadmin')
def main_command(bot, trigger):
    maincommandused = trigger.group(1)
    subcommand = get_trigger_arg(triggerargsarray, '3')
    instigator = trigger.nick
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    botownerarray, operatorarray, voicearray, adminsarray = special_users(bot)
    inchannel = trigger.sender
    if maincommandused.endswith('admin') and instigator not in adminsarray:
        bot.notice(instigator + "This is an admin only function.", instigator)
    elif maincommandused.endswith('admin') and inchannel.startswith("#"):
        bot.notice(instigator + "This admin function must be used in Privmsg.", instigator)
    elif maincommandused.endswith('admin') and instigator in adminsarray:
        admin_functions(bot, trigger, triggerargsarray)
    else:
        allowedcommandsarray = ['on','off']
        if not enablestatus or subcommand in allowedcommandsarray:
            user_functions(bot, trigger, triggerargsarray)
        
def admin_functions(bot, trigger, triggerargsarray):
    bot.say('admin')
        
def user_functions(bot, trigger, triggerargsarray):
    now = time.time()
    bot.say('user')
    
        

        
        
    
