##to be added to spicebot shared after testing
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel import module, tools
import sys
import os
import random
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
import Spicebucks
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('testtarget')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    istarget,targetmsg =targetcheck(bot,trigger.nick,get_trigger_arg(triggerargsarray, 1))
    if istarget ==1:
        bot.say("Target is valid")  
    else:
        bot.say(targetmsg)
##copy below this line into spicbotshared when it is working##

####################################
## Check if target##
####################################
def targetcheck(bot, target,instigator):
    validtarget = 0
    validtargetmsg = ''
    for channel in bot.channels:
    botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
    botuseron=[]
    for u in bot.users:
        if u in botusersarray and u != bot.nick:
            botuseron.append(u)   
    if not target:
        validtargetmsg = str(instigator + ", you must specify a target.")       
    else:
        if target == bot.nick:
            validtargetmsg = str(instigator + ", " + target + " can't be targeted.")
        elif target == instigator:       
            validtargetmsg = str(instigator + ", "is the target")
             validtarget=2            
            
        elif not target.lower() in [u.lower() for u in botuseron]:
            validtargetmsg = str(instigator + " " + target +  "isn't a valid target")            
        else:
            validtarget = 1
    return validtarget, validtargetmsg
