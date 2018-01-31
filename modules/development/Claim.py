#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import datetime
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('claim')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    
    instigator = trigger.nick
    channel = trigger.sender
    target = get_trigger_arg(triggerargsarray, 1)
    inchannel = trigger.sender
    if not inchannel.startswith("#"):
        bot.say("Claims must be done in channel")
    elif not target:
        bot.say("Who do you want to claim?")
    elif target == instigator:
        bot.say("You can't claim yourself!")
    elif target == bot.nick:
        bot.say("I have already been claimed by " + bot.owner +"!")
    elif target.lower() not in bot.privileges[channel.lower()]:
        bot.say("I'm not sure who that is.")
    elif trigger.nick == 'IT_Sean':
        bot.say(instigator + ' releases the contents of his bladder on ' + target + '! All should recognize this profound claim of ownership upon ' + claimed +'!')
    else:
       claimedby = bot.db.get_nick_value(target,'claimed') or ''
       claimdate = bot.db.get_nick_value(target, 'claimdate') or 0
       now = datetime.datetime.now()
       if claimedby == '':
           bot.say(instigator + ' urinates on ' + target + '! Claimed!')
           bot.db.set_nick_value(target,'claimed',instigator)
           bot.db.set_nick_value(target,'claimdate',now)
       else:
           bot.say(target + " has already been claimed by " + claimedby + ", so back off")
           #righnow=now.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
           #lastcliam = claimdate.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
           #daysincelastclaim = (rightnow-lastclaim).days
           #bot.say(str(dayssinceclaim))
          # if dayssinceclaim < 30:
            
           #else:      
            #   bot.say(instigator + " urinates on " + target + "! The claim has been stolen from " + str(lastclaimedby) + "!")
             #  bot.db.set_nick_value(target,'claimed',instigator)
              # bot.db.set_nick_value(target,'claimdate',now)
        
