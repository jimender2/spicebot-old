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
    # Names/nicks for code
    instigator = trigger.nick
    owner = bot.config.core.owner
    mastername = bot.db.get_nick_value(instigator,'claimed') or ''
    target = get_trigger_arg(bot, triggerargsarray, 1)
    admintarget = get_trigger_arg(bot, triggerargsarray, 2)
    masterurinator = 'IT_Sean'
    
    # Names of channel
    inchannel = trigger.sender
    channel = trigger.sender
    
    # Dates for usage
    todaydate = datetime.date.today()
    storedate = str(todaydate)
    
    # Good to claim?
    okaytoclaim = 1
    
    # Days before reclaim available
    maxtime = 7
    
    # Spicebuck reward values
    firstclaim = 5
    renewclaim = 2
    stolenclaim = 10
    masterclaim = 5 #take, not give
    
    # Make sure claims happen in channel, not privmsg
    if not inchannel.startswith("#"):
        okaytoclaim = 0
        bot.say("Claims must be done in channel")
        
    # Handle if no target is specified
    if not target:
        okaytoclaim = 0
        bot.say("Who do you want to claim?")
        
    # Check if somebody is claimed, return if/when
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
    
    # Bot admins can reset claims
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

    # Can't claim yourself
    elif target == instigator:
        okaytoclaim = 0
        bot.say("You can't claim yourself!")
        
    # Can't claim the bot
    elif target == bot.nick:
        okaytoclaim = 0
        bot.say("I have already been claimed by " + owner +"!")
    
    # Can't claim your claimant
    elif target == mastername:
        okaytoclaim = 0
        bot.action("facepalms")
        bot.say("You can't claim " + target + ", "+ instigator + ". They already have a claim on you.")
        # Take Spicebucks from instigator (masterclaim)
        Spicebucks.spicebucks(bot, instigator, 'minus', masterclaim)
    
    # Can't claim everyone at once
    if target == 'everyone':
        okaytoclaim = 0
        bot.say(instigator + " couldn't decide where to aim and pisses everywhere!")
    # If the target is not online OR a subcommand, handle it
    elif target.lower() not in bot.privileges[channel.lower()] and target != 'reset': 
        bot.say("I'm not sure who that is.") 
    
    # Input checks out. Verify dates and go ahead.
    elif okaytoclaim:
        claimedby = bot.db.get_nick_value(target,'claimed') or ''
        # First time claimed
        if claimedby == '':
            if instigator == masterurinator:
                message = instigator + " releases the contents of his bladder on " + target + "! All should recognize this profound claim of ownership upon " + target +"!"
            else:
                message = instigator + " urinates on " + target + "! Claimed!"
            bot.say(message)
            bot.db.set_nick_value(target,'claimed',instigator)
            bot.db.set_nick_value(target,'claimdate',storedate)
            # Pay instigator Spicebucks (firstclaim)
            Spicebucks.spicebucks(bot, instigator, 'plus', firstclaim)
            
        # Renewed claim
        elif claimedby == instigator:
            claimdate = bot.db.get_nick_value(target, 'claimdate') or '1999-12-31'
            datea = arrow.get(todaydate)
            dateb = arrow.get(claimdate)
            timepassed = datea - dateb
            dayspassed = timepassed.days
            if timepassed.days > int(maxtime):
                if instigator == masterurinator:
                    message = instigator + " releases the contents of his bladder on " + target + " again! All should recognize this almighty renewal of ownership over " + target + "!"
                else:
                    message = instigator + " urinates on " + target + " again! The claim has been renewed!"
                bot.say(message)
                bot.db.set_nick_value(target,'claimed',instigator)
                bot.db.set_nick_value(target,'claimdate',storedate)
                # Pay instigator Spicebucks (renewclaim)
                Spicebucks.spicebucks(bot, instigator, 'plus', renewclaim)
            else:
                bot.say(instigator + ", you already claimed " + target +".")
        else:
            # Stolen claim
            claimdate = bot.db.get_nick_value(target, 'claimdate') or '1999-12-31'
            datea = arrow.get(todaydate)
            dateb = arrow.get(claimdate)
            timepassed = datea - dateb
            dayspassed = timepassed.days
            if timepassed.days > int(maxtime):
                if instigator == masterurinator:
                    message = instigator + " empties their bladder all over " + target + "! The claim of " + str(claimedby) + " has been overpowered by " + instigator + "!"
                else:
                    message = instigator + " urinates on " + target + "! The claim has been stolen from " + claimedby + "!"
                bot.say(message)
                bot.db.set_nick_value(target,'claimed',instigator)
                bot.db.set_nick_value(target,'claimdate',storedate)
                # Pay instigator Spicebucks (stolenclaim)
                Spicebucks.spicebucks(bot, instigator, 'plus', stolenclaim)
            else:
                bot.say(target + " has already been claimed by " + str(claimedby) + ", so back off!")
    else:
        bot.say(bot.nick + " had an issue with their aim and peed absolutely everywhere!")
