#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import datetime
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

devbot = 'dev'
botdevteam = ['deathbybandaid','DoubleD','Mace_Whatdo','dysonparkes','PM','under_score']

## Prerun stripped down for now

## This runs for every custom module and decides if the module runs or not
def spicebot_prerun(bot,trigger):
    
    ## Custom args
    triggerargsarray = create_args_array(trigger.group(2))
    
    ## time
    now = time.time()
    
    ## used to circumvent
    commandused = trigger.group(1)
    
    ## Get Name Of Channel
    botchannel = trigger.sender
    
    ## Nick of user operating command
    instigator = trigger.nick
    
    ## Enable Status default is 1 = don't run
    #enablestatus = 1
    enablestatus = 0
    
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
        for u in bot.channels[channel.lower()].users:
            allusersinroomarray.append(u)
            udisenable = get_botdatabase_value(bot, u, 'disenable')
            if u != bot.nick and udisenable:
                if u.lower() in bot.config.core.owner.lower():
                    botownerarray.append(u)
                if bot.privileges[channel.lower()][u] == OP:
                    operatorarray.append(u)
                if bot.privileges[channel.lower()][u.lower()] == VOICE:
                    voicearray.append(u)
                if u in bot.config.core.admins:
                    adminsarray.append(u)
    return botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray, channel

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
            randomselected = random.randint(0,len(triggerargsarray) - 1)
            triggerarg = str(triggerargsarray [randomselected])
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

###########
## Tools ##
###########

def diceroll(howmanysides):
    diceroll = randint(0, howmanysides)
    return diceroll
