import sopel.module
import sopel
from sopel import module, tools
import random
from random import randint
import time
import re
import sys
import os
from os.path import exists
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

relativepath = "data/weapons.txt"
weaponslocker = os.path.join(moduledir, relativepath)

TIMEOUT = 180
TIMEOUTC = 40
ALLCHAN = 'entirechannel'
OPTTIMEOUT = 3600

## React to /me (ACTION) challenges
#@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
#@module.intent('ACTION')
#@module.require_chanmsg
#def challenge_action(bot, trigger):
#    enablestatus = spicebot_prerun(bot, trigger)
#    if not enablestatus:
#        return challenge(bot, trigger.sender, trigger.nick, trigger.group(1))

####################
## Main Operation ##
####################

@sopel.module.commands('challengea','duela')
@module.require_chanmsg
def challenge_cmd(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        return challenge(bot, trigger)
        
def challenge(bot, trigger):
    options = str("")
    if not trigger.group(2):
        bot.notice(instigator + ", Who did you want to challenge? Other Options are: " + str(options), instigator)
    else:
        target = trigger.group(2)
        if target == '':
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
