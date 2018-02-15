#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import arrow
import sys
import os
import datetime
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *
import Spicebucks

@sopel.module.commands('claim')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    owner = bot.config.core.owner
    target = get_trigger_arg(triggerargsarray, 1)
    admintarget = get_trigger_arg(triggerargsarray, 2)
    inchannel = trigger.sender
    channel = trigger.sender
    todaydate = datetime.date.today()  
    storedate = str(todaydate)
    okaytoclaim = 1
    maxtime = 7
    mastername = bot.db.get_nick_value(instigator,'claimed') or ''
    if not inchannel.startswith("#"):
        okaytoclaim = 0
        bot.say("Claims must be done in channel")
    elif not target:
        okaytoclaim = 0
        bot.say("Who do you want to claim?")
    elif target == 'check':
        okaytoclaim = 0
        if not admintarget:
            admintarget = instigator
        claimdate = bot.db.get_nick_value(admintarget, 'claimdate')
        claimedby = bot.db.get_nick_value(admintarget,'claimed')
        if not claimedby:
            if admintarget == instigator:
                bot.say("Nobody has a claim on you yet, " + str(instigator) +".")
            else:
                bot.say("Nobody appears to have claimed " + str(admintarget) + " yet, " + str(instigator) + ".")
        else:
            if admintarget == instigator:
                bot.say("You were claimed by " + str(claimedby) + " on " + str(claimdate) +", " + str(instigator) + ".")
            else:
                bot.say(str(admintarget) + " was claimed by " + str(claimedby) + " on " + str(claimdate) +", " + instigator + ".")
    elif target == instigator:
        okaytoclaim = 0
        bot.say("You can't claim yourself!")
    elif target == bot.nick:
        okaytoclaim = 0
        bot.say("I have already been claimed by " + owner +"!")
    elif target == mastername:
        okaytoclaim = 0
        bot.action("facepalms")
        bot.say("You can't claim " + target + ", "+ instigator + ". They already have a claim on you.")
    elif target == 'reset':
        okaytoclaim = 0
        if trigger.admin:
            if not admintarget:
                bot.say("Please specify someone to reset claim on.")
            elif admintarget.lower() not in bot.privileges[channel.lower()]:
                bot.say("I'm not sure who that is.")
            else:
                bot.db.set_nick_value(admintarget,'claimed','')
                bot.db.set_nick_value(admintarget,'claimdate','')
                bot.say("Claim info for " + admintarget + " reset on " + str(todaydate))
        else:
            bot.say("This function is only available for bot admins.")
    elif target.lower() not in bot.privileges[channel.lower()] and target != 'reset':
        bot.say("I'm not sure who that is.")
    elif isntigator == 'IT_Sean':
        okaytoclaim = 0
        claimedby = bot.db.get_nick_value(target,'claimed') or ''
        if claimedby == '':
            bot.say(instigator + ' releases the contents of his bladder on ' + target + '! All should recognize this profound claim of ownership upon ' + claimed +'!')
            bot.db.set_nick_value(target,'claimed',instigator)
            bot.db.set_nick_value(target,'claimdate',storedate)
        else: 
            bot.say(target + " has already been claimed by " + str(claimedby) + ", so back off!")
    elif okaytoclaim:
        claimedby = bot.db.get_nick_value(target,'claimed') or ''
        if claimedby == '':
            bot.say(instigator + ' urinates on ' + target + '! Claimed!')
            bot.db.set_nick_value(target,'claimed',instigator)
            bot.db.set_nick_value(target,'claimdate',storedate)
        elif claimedby == instigator:
            claimdate = bot.db.get_nick_value(target, 'claimdate') or '1999-12-31'
            datea = arrow.get(todaydate)
            dateb = arrow.get(claimdate)
            timepassed = datea - dateb
            dayspassed = timepassed.days
            if timepassed.days > int(maxtime):
                bot.say(instigator + " urinates on " + target + " again! The claim has been renewed!")
                bot.db.set_nick_value(target,'claimed',instigator)
                bot.db.set_nick_value(target,'claimdate',storedate)
            else:
                bot.say(instigator + ", you already claimed " + target +".")
        else:
            claimdate = bot.db.get_nick_value(target, 'claimdate') or '1999-12-31'
            datea = arrow.get(todaydate)
            dateb = arrow.get(claimdate)
            timepassed = datea - dateb
            dayspassed = timepassed.days
            if timepassed.days > int(maxtime):
                if claimedby == '':
                    bot.say(instigator + " urinates on " + target + "! Claimed!")
                else:
                    bot.say(instigator + " urinates on " + target + "! The claim has been stolen from " + claimedby + "!")
                bot.db.set_nick_value(target,'claimed',instigator)
                bot.db.set_nick_value(target,'claimdate',storedate)
            else:
                bot.say(target + " has already been claimed by " + str(claimedby) + ", so back off!")
    else:
        bot.say(bot.nick + " had an issue with their aim and peed absolutely everywhere!")
