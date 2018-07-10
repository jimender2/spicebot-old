#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

#author jimender2

commandarray = ["yesterday","today","last"]

@sopel.module.commands('til')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'til')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick

    databasekey = 'til'
    command = get_trigger_arg(bot, triggerargsarray, 1)
    inputstring = get_trigger_arg(bot, triggerargsarray, '2+')
    existingarray = get_botdatabase_value(bot, bot.nick, databasekey) or []
    if command in commandarray:
        if command == "add":
            if inputstring not in existingarray:
                adjust_botdatabase_array(bot, bot.nick, inputstring, databasekey, 'add')
                message = "Added to database."
		bot.say(message)
            else:
                message = "That response is already in the database."
		bot.say(message)
        elif command == "remove":
            if inputstring not in existingarray:
                message = "That response was not found in the database."
		bot.say(message)
            else:
                adjust_botdatabase_array(bot, bot.nick, inputstring, databasekey, 'del')
                message = "Removed from database."
		bot.say(message)
        elif command == "count":
		messagecount = len(existingarray)
		message = "There are currently " + str(messagecount) + " responses for that in the database."
		bot.say(message)

        elif command == "last":
		message = get_trigger_arg(bot, existingarray, "last")
		bot.say(message)
    else:
        weapontype = get_trigger_arg(bot, existingarray, "random") or ''
        if weapontype == '':
        	message = "No response found. Have any been added?"
	target = get_trigger_arg(bot, triggerargsarray, 1)
	reason = get_trigger_arg(bot, triggerargsarray, '2+')
	msg = "a " + weapontype

	# No target specified
	if not target:
		bot.say("Who/what would you like to til?")

	# Cannot kill spicebot
	elif target == bot.nick:
		bot.say("You cannot kill a nonliving entity")

	# Cannot kill self
	elif target == instigator:
		message = "Killing yourself would be suicide, " + instigator + ", not til. Idiot."
		bot.say(message)

	# Target is fine
	else:
		if not reason:
			message = instigator + " tils " + target + " with " + msg + "."
        		bot.say(message)
		else:
			message = instigator + " tils " + target + " with " + msg + " for " + reason + "."
        		bot.say(message)



def get_botdatabase_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

def set_botdatabase_value(bot, nick, databasekey, value):
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)

def reset_botdatabase_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, None)
    
def adjust_botdatabase_value(bot, nick, databasekey, value):
    oldvalue = get_botdatabase_value(bot, nick, databasekey) or 0
    databasecolumn = str(databasekey)
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