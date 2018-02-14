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
import urllib
from os.path import exists

devbot = 'dev' ## If using a development bot and want to bypass commands, this is what the bots name ends in
botdevteam = ['deathbybandaid','DoubleD','Mace_Whatdo','dysonparkes','PM','under_score']

## This runs for every custom module and decides if the module runs or not
def spicebot_prerun(bot,trigger,commandused):
    
    ## Get Name Of Current Channel
    botchannel = trigger.sender
    
    ## Custom args
    try:
        triggerargsarray = get_trigger_arg(trigger.group(2), 'create')
    except IndexError:
        triggerargsarray = get_trigger_arg(trigger.group(1), 'create')
    
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

####################################
## Array/List/String Manipulation ##
####################################

## Hub
def get_trigger_argnew(bot, inputs, outputtask):
    ## Create
    if outputtask == 'create':
        return create_array(bot, inputs)
    ## reverse
    if outputtask == 'reverse':
        return reverse_array(bot, inputs)
    ## Comma Seperated List
    if outputtask == 'list':
        return list_array(bot, inputs)
    if outputtask == 'random':
        return random_array(bot, inputs)
    ## Last element
    if outputtask == 'last':
        return last_array(bot, inputs)
    ## Complete String
    if outputtask == 0 or outputtask == 'complete' or outputtask == 'string':
        return string_array(bot, inputs)
    ## Number
    if str(outputtask).isdigit():
        return number_array(bot, inputs, outputtask)
    ## Exlude from array
    if str(outputtask).endswith("!"):
        return excludefrom_array(bot, inputs, outputtask)
    ## Inclusive range starting at
    if str(outputtask).endswith("+"):
        return incrange_plus_array(bot, inputs, outputtask)
    ## Inclusive range ending at
    if str(outputtask).endswith("-"):
        return incrange_minus_array(bot, inputs, outputtask)
    ## Exclusive range starting at
    if str(outputtask).endswith(">"):
        return excrange_plus_array(bot, inputs, outputtask)
    ## Exclusive range ending at
    if str(outputtask).endswith("<"):
        return excrange_minus_array(bot, inputs, outputtask)
    ## Range Between Numbers
    if "^" in str(outputtask):
        return rangebetween_array(bot, inputs, outputtask)
    string = ''
    return string
    
## Convert String to array
def create_array(bot, inputs):
    if isinstance(inputs, list):
        string = ''
        for x in inputs:
            if string != '':
                string = str(string + " " + str(x))
            else:
                string = str(x)
        inputs = string
    outputs = []
    if inputs:
        for word in inputs.split():
            outputs.append(word)
    return outputs

## Convert Array to String
def string_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    for x in inputs:
        if string != '':
            string = str(string + " " + str(x))
        else:
            string = str(x)
    return string

## output reverse order
def reverse_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    if len(inputs) == 1:
        return inputs
    outputs = []
    if inputs == []:
        return outputs
    for d in inputs:
        outputs.append(d)
    outputs.reverse()
    return outputs

## Comma Seperated List
def list_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    for x in inputs:
        if string != '':
            string  = str(string  + ", " + x)
        else:
            string  = str(x)
    return string

## Random element
def random_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    temparray = []
    for d in inputs:
        temparray.append(d)
    shuffledarray = random.shuffle(temparray)
    randomselected = random.randint(0,len(temparray) - 1)
    string = str(temparray [randomselected])
    return string

## Last element
def last_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    string = inputs[len(inputs)-1]
    return string

def number_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if str(number).isdigit():
        numberadjust = int(number) -1
        if numberadjust< len(inputs) and numberadjust >= 0:
            number = int(number) - 1
            string = inputs[number]
    return string

def range_array(bot, inputs, rangea, rangeb):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    if int(rangeb) == int(rangea):
        return number_array(bot, inputs, rangeb)
    if int(rangeb) < int(rangea):
        tempa, tempb = rangeb, rangea
        rangea, rangeb = tempa, tempb
    if int(rangea) < 1:
        rangea = 1
    if int(rangeb) > len(inputs):
        rangeb = len(inputs)
    for i in range(int(rangea),int(rangeb) + 1):
        arg = number_array(bot, inputs, i)
        if string != '':
            string = str(string + " " + arg)
        else:
            string = str(arg)
    return string

def excludefrom_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if str(number).endswith("!"):
        number = re.sub(r"!", '', str(number))
    if str(number).isdigit():
        for i in range(1,len(inputs)):
            if int(i) != int(number):
                arg = number_array(bot, inputs, i)
                if string != '':
                    string = str(string + " " + arg)
                else:
                    string = str(arg)
    return string

def rangebetween_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if "^" in str(number):
        rangea = number.split("^", 1)[0]
        rangeb = number.split("^", 1)[1]
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

def incrange_plus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith("+"):
        rangea = re.sub(r"\+", '', str(number))
        rangeb = len(inputs)
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

def incrange_minus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith("-"):
        rangea = 1
        rangeb = re.sub(r"-", '', str(number))
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

def excrange_plus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith(">"):
        rangea = re.sub(r">", '', str(number))
        rangea = int(rangea) + 1
        rangeb = len(inputs)
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

def excrange_minus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith("<"):
        rangea = 1
        rangeb = re.sub(r"<", '', str(number))
        rangeb = int(rangeb) - 1
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

#############
## Old arg ##
#############

def create_args_array(fullstring):
    triggerargsarray = []
    if fullstring:
        for word in fullstring.split():
            triggerargsarray.append(word)
    return triggerargsarray

def get_trigger_arg(triggerargsarray, number):
    if number == 'create':
        triggerargsarraynew = []
        if triggerargsarray:
            for word in triggerargsarray.split():
                triggerargsarraynew.append(word)
        return triggerargsarraynew
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

def reset_botdatabase_value(bot, nick, databasekey):
    databasecolumn = str('spicebot_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, None)
    
def adjust_botdatabase_value(bot, nick, databasekey, value):
    oldvalue = get_botdatabase_value(bot, nick, databasekey) or 0
    databasecolumn = str('spicebot_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))
   
def get_botdatabase_array_total(bot, nick, databasekey):
    array = get_botdatabase_value(bot, nick, databasekey) or []
    entriestotal = len(array)
    return entriestotal

def adjust_botdatabase_array(bot, nick, entries, databasekey, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
    adjustarray = get_botdatabase_value(bot, nick, databasekey) or []
    adjustarraynew = []
    for x in adjustarray:
        adjustarraynew.append(x)
    reset_botdatabase_value(bot, nick, databasekey)
    adjustarray = []
    if adjustmentdirection == 'add':
        for y in entries:
            if y not in adjustarraynew:
                adjustarraynew.append(y)
    elif adjustmentdirection == 'del':
        for y in entries:
            if y in adjustarraynew:
                adjustarraynew.remove(y)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        reset_botdatabase_value(bot, nick, databasekey)
    else:
        set_botdatabase_value(bot, nick, databasekey, adjustarray)
        
############################
## Fix unicode in strings ##
############################

def unicode_string_cleanup(string):
    for r in (("\u2013", "-"), ("\u2019", "'"), ("\u2026", "...")):
        string = string.replace(*r)
    return string

def quote(string, safe='/'):
    # modified urllib2.quote that handles unicode properly
    if sys.version_info.major < 3:
        if isinstance(string, unicode):
            string = string.encode('utf8')
        string = urllib.quote(string, safe.encode('utf8'))
    else:
        string = urllib.parse.quote(str(string), safe)
    return string
    
##########
## Time ##
##########

def enoughdaysbetween(earlydate, laterdate, numberofdays):
    datea = arrow.get(laterdate)
    dateb = arrow.get(earlydate)
    timepassed = datea - dateb
    dayspassed = timepassed.days
    if timepassed.days > int(numberofdays):
        longenough = 1
    else:
        longenough = 0
    return longenough

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
