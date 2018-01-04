#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import datetime
import arrow
from sopel.tools import Identifier
from sopel.tools.time import get_timezone, format_time
from sopel.module import commands, rule, priority, thread
import sopel.module
from sopel import module, tools
from sopel.module import OP
from sopel.module import ADMIN
from sopel.module import VOICE
from sopel.module import event, rule
import time
import os
import sys, re
import fnmatch
import random
from os.path import exists

devbot = 'dev' ## If using a development bot and want to bypass commands, this is what the bots name ends in
botdevteam = ['deathbybandaid','DoubleD','Mace_Whatdo','dysonparkes','PM','under_score']

## This runs for every custom module and decides if the module runs or not
def spicebot_prerun(bot,trigger,commandused):
    
    ## Get Name Of Current Channel
    botchannel = trigger.sender
    
    ## Custom args
    try:
        triggerargsarray = create_args_array(trigger.group(2))
    except IndexError:
        triggerargsarray = create_args_array(trigger.group(1))
    
    ## Nick of user operating command
    instigator = trigger.nick

    ## time
    now = time.time()
    
    ## Enable Status default is 1 = don't run
    enablestatus = 1
    
    ## User was Blocked by a bot.admin or an OP
    blockedusersarray = get_botdatabase_value(bot, botchannel, 'blockedusers') or []
    if instigator in blockedusersarray:
        bot.notice(instigator + ", it looks like you have been blocked from using commands in " + botchannel,instigator)
        return enablestatus, triggerargsarray
    
    ## Channel activated status
    if botchannel.startswith("#"):
        channelmodulesarray = get_botdatabase_value(bot, botchannel, 'channelmodules') or []
        if commandused not in channelmodulesarray:
            bot.notice(instigator + ", it looks like the " + str(commandused) + " command has not been enabled in " + botchannel + ".",instigator)
            return enablestatus, triggerargsarray
    
    ## Bot Enabled Status (now in an array)
    botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
    
    ## Bot warned Status (now in an array)
    botwarnedarray = get_botdatabase_value(bot, bot.nick, 'botuserswarned') or []
    
    if instigator not in botusersarray and instigator not in botwarnedarray:
        bot.notice(instigator + ", you have to run .spicebot on to allow her to listen to you. For help, see the wiki at https://github.com/deathbybandaid/sopel-modules/wiki/Using-the-Bot.",instigator)
    elif instigator not in botusersarray and instigator in botwarnedarray:
        bot.notice(instigator + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBot and ##SpiceBotTest.",instigator)
    

    ## Run Module if above checks pass
    else:
        enablestatus = 0
        increment_counter(bot, trigger,commandused)

    ## Send Status Forward
    return enablestatus, triggerargsarray



#####################################################################################################################################
## Below This Line are Shared Functions
#####################################################################################################################################

###################
## Special Users ##
###################

def special_users(bot):
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray = [], [], [], [], []
    for channel in bot.channels:
        for u in bot.users:
            allusersinroomarray.append(u)
            if u != bot.nick:
                
                try:
                    if u.lower() in bot.config.core.owner.lower():
                        botownerarray.append(u)
                except KeyError:
                    dumbyvar = 1
                
                try:
                    if bot.privileges[channel.lower()][u.lower()] == OP:
                        operatorarray.append(u)
                except KeyError:
                    dumbyvar = 1
                
                try:
                    if bot.privileges[channel.lower()][u.lower()] == VOICE:
                        voicearray.append(u)
                except KeyError:
                    dumbyvar = 1
                
                try:
                    if u in bot.config.core.admins:
                        adminsarray.append(u)
                except KeyError:
                    dumbyvar = 1
    return botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray

#####################
## Module Counters ##
#####################

def increment_counter(bot, trigger, commandused):
    instigator = trigger.nick # Who to increment for
    botchannel = trigger.sender # Channel to increment for
    adjust_botdatabase_value(bot, botchannel, str(commandused + "moduleusage"), 1) ## Channel usage of specific module
    adjust_botdatabase_value(bot, botchannel, "spicebottotalusage", 1) ## Channel usage of bot overall
    adjust_botdatabase_value(bot, instigator, str(commandused + "moduleusage"), 1) ## User usage of specific module
    adjust_botdatabase_value(bot, instigator, "spicebottotalusage", 1) ## User usage of bot overall

##########
## ARGS ##
##########

def create_args_array(fullstring):
    triggerargsarray = []
    if fullstring:
        for word in fullstring.split():
            triggerargsarray.append(word)
    return triggerargsarray

def get_trigger_arg(triggerargsarray, number):
    totalarray = len(triggerargsarray)
    totalarray = totalarray + 1
    triggerarg = ''
    if "^" in str(number) or number == 0 or str(number).endswith("+") or str(number).endswith("-") or str(number).endswith("<") or str(number).endswith(">"):
        if str(number).endswith("+"):
            rangea = re.sub(r"\+", '', str(number))
            rangea = int(rangea)
            rangeb = totalarray
        elif str(number).endswith("-"):
            rangea = 1
            rangeb = re.sub(r"-", '', str(number))
            rangeb = int(rangeb) + 1
        elif str(number).endswith(">"):
            rangea = re.sub(r">", '', str(number))
            rangea = int(rangea) + 1
            rangeb = totalarray
        elif str(number).endswith("<"):
            rangea = 1
            rangeb = re.sub(r"<", '', str(number))
            rangeb = int(rangeb)
        elif "^" in str(number):
            rangea = number.split("^", 1)[0]
            rangeb = number.split("^", 1)[1]
            rangea = int(rangea)
            rangeb = int(rangeb) + 1
        elif number == 0:
            rangea = 1
            rangeb = totalarray
        if rangea <= totalarray:
            for i in range(rangea,rangeb):
                arg = get_trigger_arg(triggerargsarray, i)
                if triggerarg != '':
                    triggerarg = str(triggerarg + " " + arg)
                else:
                    triggerarg = str(arg)
    elif number == 'last':
        if totalarray > 1:
            totalarray = totalarray -2
            triggerarg = str(triggerargsarray[totalarray])
    elif str(number).endswith("!"):
        number = re.sub(r"!", '', str(number))
        for i in range(1,totalarray):
            if int(i) != int(number):
                arg = get_trigger_arg(triggerargsarray, i)
                if triggerarg != '':
                    triggerarg = str(triggerarg + " " + arg)
                else:
                    triggerarg = str(arg)
    elif number == 'random':
        if totalarray > 1:
            try:
                shuffledarray = random.shuffle(triggerargsarray)
                randomselected = random.randint(0,len(shuffledarray) - 1)
                triggerarg = str(shuffledarray [randomselected])
            except TypeError:
                triggerarg = get_trigger_arg(triggerargsarray, 1)
        else:
            triggerarg = get_trigger_arg(triggerargsarray, 1)
    elif number == 'list':
        for x in triggerargsarray:
            if triggerarg != '':
                triggerarg  = str(triggerarg  + ", " + x)
            else:
                triggerarg  = str(x)
    else:
        number = int(number) - 1
        try:
            triggerarg = triggerargsarray[number]
        except IndexError:
            triggerarg = ''
    return triggerarg

##############
## Database ##
##############

def get_botdatabase_value(bot, nick, databasekey):
    databasecolumn = str('spicebot_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

def set_botdatabase_value(bot, nick, databasekey, value):
    databasecolumn = str('spicebot_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)
    
def adjust_botdatabase_value(bot, nick, databasekey, value):
    oldvalue = get_botdatabase_value(bot, nick, databasekey) or 0
    databasecolumn = str('spicebot_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))
   
def get_botdatabase_array_total(bot, nick, databasekey):
    array = get_botdatabase_value(bot, nick, databasekey) or []
    entriestotal = len(array)
    return entriestotal

def adjust_database_array(bot, nick, entry, databasekey, adjustmentdirection):
    adjustarray = get_botdatabase_value(bot, nick, databasekey) or []
    adjustarraynew = []
    for x in adjustarray:
        adjustarraynew.append(x)
    set_botdatabase_value(bot, nick, databasekey, None)
    adjustarray = []
    if adjustmentdirection == 'add':
        if entry not in adjustarraynew:
            adjustarraynew.append(entry)
    elif adjustmentdirection == 'del':
        if entry in adjustarraynew:
            adjustarraynew.remove(entry)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        set_botdatabase_value(bot, nick, databasekey, None)
    else:
        set_botdatabase_value(bot, nick, databasekey, adjustarray)

############################
## Fix unicode in strings ##
############################

def unicode_string_cleanup(string):
    for r in (("\u2013", "-"), ("\u2019", "'"), ("\u2026", "...")):
        string = string.replace(*r)
    return string
    
##########
## Time ##
##########

def get_timesince(bot, nick, databasekey):
    now = time.time()
    last = get_botdatabase_value(bot, nick, databasekey) or 0
    return abs(now - int(last))

def get_timeuntil(nowtime, futuretime):
    a = arrow.get(nowtime)
    b = arrow.get(futuretime)
    timecompare = (b.humanize(a, granularity='auto'))
    return timecompare

def hours_minutes_seconds(countdownseconds):
    time = float(countdownseconds)
    year = time // (365 * 24 * 3600)
    time = time % (365 * 24 * 3600)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minute = time // 60
    time %= 60
    second = time
    displaymsg = ''
    timearray = ['year','day''hour','minute','second']
    for x in timearray:
        currenttimevar = eval(x)
        if currenttimevar >= 1:
            timetype = x
            if currenttimevar > 1:
                timetype = str(x+"s")
            displaymsg = str(displaymsg + str(int(currenttimevar)) + " " + timetype + " ")
    return displaymsg

###########
## Tools ##
###########

def diceroll(howmanysides):
    diceroll = randint(0, howmanysides)
    return diceroll
