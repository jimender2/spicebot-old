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
import sys
import re
import fnmatch
import random
import urllib
from os.path import exists
reload(sys)
sys.setdefaultencoding('utf-8')

import spicemanip


osd_limit = 420  # Ammount of text allowed to display per line

devbot = 'dev'  # If using a development bot and want to bypass commands, this is what the bots name ends in
botdevteam = ['deathbybandaid', 'DoubleD', 'Mace_Whatdo', 'dysonparkes', 'PM', 'under_score']


# This runs for every custom module and decides if the module runs or not
def spicebot_prerun(bot, trigger, commandused):

    # Dyno Classes
    botcom = class_create('bot')

    # Enable Status default is 1 = don't run
    botcom.enablestatus = 1

    # Custom args
    try:
        botcom.triggerargsarray = spicemanip.main(trigger.group(2), 'create')
    except IndexError:
        botcom.triggerargsarray = spicemanip.main(trigger.group(1), 'create')

    botcom.instigator = trigger.nick

    # time
    botcom.now = time.time()

    # User
    botcom = bot_command_users(bot, botcom)

    # Channels
    botcom = bot_command_channels(bot, botcom, trigger)

    # User was Blocked by a bot.admin or an OP
    blockedusersarray = get_database_value(bot, botcom.channel_current, 'users_blocked') or []
    if botcom.instigator in blockedusersarray:
        osd(bot, botcom.instigator, 'notice', "It looks like you have been blocked from using commands in " + botcom.channel_current+".")
        return botcom.enablestatus, botcom.triggerargsarray, botcom, botcom.instigator

    # devmode bypass
    devenabledchannels = get_database_value(bot, bot.nick, 'channels_dev') or []
    if botcom.channel_current in devenabledchannels:
        botcom.enablestatus = 0
        return botcom.enablestatus, botcom.triggerargsarray, botcom, botcom.instigator

    # Channel activated status
    if botcom.channel_current.startswith("#"):
        channelmodulesarray = get_database_value(bot, botcom.channel_current, 'modules_enabled') or []
        if commandused not in channelmodulesarray:
            if botcom.instigator in botcom.opadmin:
                adjust_database_array(bot, botcom.channel_current, commandused, 'modules_enabled', 'add')
            else:
                osd(bot, botcom.instigator, 'notice', "it looks like the " + str(commandused) + " command has not been enabled in " + botcom.channel_current+".")
                return botcom.enablestatus, botcom.triggerargsarray, botcom, botcom.instigator

    # Bot Enabled Status (botcom.now in an array)
    botusersarray = get_database_value(bot, bot.nick, 'botusers') or []

    # bot_opted_users = get_database_value(bot, bot.nick, 'users_opted') or []
    # if botcom.instigator not in bot_opted_users:
    #    osd(bot, botcom.instigator, 'notice', "you have to run `" + bot.nick + " on` to allow her to listen to you. For help, see the wiki at https://github.com/SpiceBot/sopel-modulesold/wiki/Using-the-Bot.")
    #    return botcom.enablestatus, botcom.triggerargsarray, botcom, botcom.instigator

    botcom.enablestatus = 0
    increment_counter(bot, trigger, commandused)

    # Send Status Forward

    return botcom.enablestatus, botcom.triggerargsarray, botcom, botcom.instigator


"""
###################################################################
# Below This Line are Shared Functions
###################################################################
"""

"""
##############
# Bot basics #
##############
"""


# Bot Nicks
def bot_config_names(bot):
    config_listing = []
    networkname = str(bot.config.core.user.split("/", 1)[1] + "/")
    validconfigsdir = str("/home/spicebot/.sopel/" + bot.nick + "/System-Files/Configs/" + networkname)
    for filename in os.listdir(validconfigsdir):
        filenameminuscfg = str(filename).replace(".cfg", "")
        config_listing.append(filenameminuscfg)
    return config_listing


# Outputs Nicks with correct capitalization
def actualname(bot, nick):
    nick_actual = str(nick)
    for u in bot.users:
        if u.lower() == str(nick).lower():
            nick_actual = u
    return nick_actual


def nick_actual(bot, nick):
    nick_actual = str(nick)
    for u in bot.users:
        if u.lower() == str(nick).lower():
            nick_actual = u
    return nick_actual


def bot_command_users(bot, botcom):
    botcom.opadmin, botcom.owner, botcom.chanops, botcom.chanvoice, botcom.botadmins, botcom.users_current = [], [], [], [], [], []

    for user in bot.users:
        botcom.users_current.append(str(user))
    adjust_database_array(bot, 'channel', botcom.users_current, 'users_all', 'add')
    botcom.users_all = get_database_value(bot, 'channel', 'users_all') or []

    for user in botcom.users_current:

        if user in bot.config.core.owner:
            botcom.owner.append(user)

        if user in bot.config.core.admins:
            botcom.botadmins.append(user)
            botcom.opadmin.append(user)

        for channelcheck in bot.channels:
            try:
                if bot.privileges[channelcheck][user] == OP:
                    botcom.chanops.append(user)
                    botcom.opadmin.append(user)
            except KeyError:
                dummyvar = 1
            try:
                if bot.privileges[channelcheck][user] == VOICE:
                    botcom.chanvoice.append(user)
            except KeyError:
                dummyvar = 1

    return botcom


def bot_command_channels(bot, botcom, trigger):
    botcom.channel_current = trigger.sender
    if not botcom.channel_current.startswith("#"):
        botcom.channel_priv = 1
        botcom.channel_real = 0
    else:
        botcom.channel_priv = 0
        botcom.channel_real = 1
    botcom.service = bot.nick
    botcom.channel_list = []
    for channel in bot.channels:
        botcom.channel_list.append(channel)
    return botcom


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


"""
###########
# Module Counters #
###########
"""


def increment_counter(bot, trigger, commandused):
    instigator = trigger.nick  # Who to increment for
    channel_current = trigger.sender  # Channel to increment for
    adjust_database_value(bot, channel_current, str(commandused + "moduleusage"), 1)  # Channel usage of specific module
    adjust_database_value(bot, channel_current, "spicebottotalusage", 1)  # Channel usage of bot overall
    adjust_database_value(bot, instigator, str(commandused + "moduleusage"), 1)  # User usage of specific module
    adjust_database_value(bot, instigator, "spicebottotalusage", 1)  # User usage of bot overall


"""
##################
# Check for target #
##################
"""


def targetcheck(bot, botcom, target, instigator):
    # Guilty until proven Innocent
    validtarget = 0  # 0 = invalid, 1 = valid 2 = instigator, 3 = bot, 4 =offline
    validtargetmsg = []
    target = target.lower()

    # Target is instigator
    if target == botcom.instigator:
        validtarget = 2
        validtargetmsg.append("Target is instigator")
        return validtarget, validtargetmsg

    if target == bot.nick:
        validtarget = 3
        validtargetmsg.append("Target is a bot")
        return validtarget, validtargetmsg
        # offline
        # if target not in [x.lower() for x in botcom.users_current] and target in [x.lower() for x in botcom.users_all]:

    # Null Target
    if not target:
        validtarget = 0
        validtargetmsg.append("You must specify a target.")
        return validtarget, validtargetmsg
    if target not in [x.lower() for x in botcom.users_current] and target in [x.lower() for x in botcom.users_all]:
        validtarget = 4
        realnick = nick_actual(bot, target)
        validtargetmsg.append(realnick + " is currently offline")
        return validtarget, validtargetmsg
    if target in [x.lower() for x in botcom.users_current]:
        validtarget = 1
        realnick = nick_actual(bot, target)
        validtargetmsg.append(realnick + " is currently online")
        return validtarget, validtargetmsg
    else:
        validtarget = 0
        validtargetmsg.append(target + " is invalid user")
        return validtarget, validtargetmsg


####################
# EASY targetcheck #
####################


def easytargetcheck(bot, botcom, target, instigator):
    # Guilty until proven Innocent
    validtarget = 'false'  # 0 = invalid, 1 = valid 2 = instigator, 3 = bot, 4 =offline
    target = target.lower()

    # Target is instigator
    if target == instigator:
        validtarget = 'instigator'
        return validtarget

    if target == bot.nick:
        validtarget = 'bot'
        return validtarget

    # Null Target
    if not target:
        validtarget = 'false'
        return validtarget
    if target not in [x.lower() for x in botcom.users_current] and target in [x.lower() for x in botcom.users_all]:
        validtarget = 'offline'
        realnick = nick_actual(bot, target)
        return validtarget
    if target in [x.lower() for x in botcom.users_current]:
        validtarget = 'online'
        realnick = nick_actual(bot, target)
        return validtarget
    else:
        validtarget = 'true'
        return validtarget


"""
##############
# Fix unicode in strings #
##############
"""


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


"""
#####
# Time #
#####
"""


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
    last = get_database_value(bot, nick, databasekey) or 0
    return abs(now - int(last))


def get_timeuntil(now, futuretime):
    a = arrow.get(now)
    b = arrow.get(futuretime)
    timecompare = (b.humanize(a, granularity='auto'))
    return timecompare


def hours_minutes_seconds(countdownseconds):
    time = float(countdownseconds)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minute = time // 60
    time %= 60
    second = time
    displaymsg = ''
    timearray = ['hour', 'minute', 'second']
    for x in timearray:
        currenttimevar = eval(x)
        if currenttimevar >= 1:
            timetype = x
            if currenttimevar > 1:
                timetype = str(x+"s")
            displaymsg = str(displaymsg + str(int(currenttimevar)) + " " + timetype + " ")
    return displaymsg


def humanized_time(countdownseconds):
    time = float(countdownseconds)
    year = time // (365 * 24 * 3600)
    time = time % (365 * 24 * 3600)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minute = time // 60
    time %= 60
    second = time
    displaymsg = ''
    timearray = ['year', 'day', 'hour', 'minute', 'second']
    for x in timearray:
        currenttimevar = eval(x)
        if currenttimevar >= 1:
            timetype = x
            if currenttimevar > 1:
                timetype = str(x+"s")
            displaymsg = str(displaymsg + str(int(currenttimevar)) + " " + timetype + " ")
    return displaymsg


def hours_minutes_secondsold(countdownseconds):
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
    timearray = ['year', 'day', 'hour', 'minute', 'second']
    for x in timearray:
        currenttimevar = eval(x)
        if currenttimevar >= 1:
            timetype = x
            if currenttimevar > 1:
                timetype = str(x+"s")
            displaymsg = str(displaymsg + str(int(currenttimevar)) + " " + timetype + " ")
    return displaymsg


"""
######
# Tools #
######
"""


def diceroll(howmanysides):
    diceroll = randint(0, howmanysides)
    return diceroll


"""
#######
# Database #
#######
"""


# Get a value
def get_database_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value


# set a value
def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)


# set a value to None
def reset_database_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, None)


# add or subtract from current value
def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey) or 0
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))


# array stored in database length
def get_database_array_total(bot, nick, databasekey):
    array = get_database_value(bot, nick, databasekey) or []
    entriestotal = len(array)
    return entriestotal


# array stored in database, add or remove elements
def adjust_database_array(bot, nick, entries, databasekey, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
    adjustarray = get_database_value(bot, nick, databasekey) or []
    adjustarraynew = []
    for x in adjustarray:
        adjustarraynew.append(x)
    reset_database_value(bot, nick, databasekey)
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
        reset_database_value(bot, nick, databasekey)
    else:
        set_database_value(bot, nick, databasekey, adjustarray)


# Database Users
def get_user_dict(bot, dynamic_class, nick, dictkey):

    # check that db list is there
    if not hasattr(dynamic_class, 'userdb'):
        dynamic_class.userdb = class_create('userdblist')
    if not hasattr(dynamic_class.userdb, 'list'):
        dynamic_class.userdb.list = []

    returnvalue = 0

    # check if nick has been pulled from db already
    if nick not in dynamic_class.userdb.list:
        dynamic_class.userdb.list.append(nick)
        nickdict = get_database_value(bot, nick, dynamic_class.default) or dict()
        createuserdict = str("dynamic_class.userdb." + nick + " = nickdict")
        exec(createuserdict)
    else:
        if not hasattr(dynamic_class.userdb, nick):
            nickdict = dict()
        else:
            nickdict = eval('dynamic_class.userdb.' + nick)

    if dictkey in nickdict.keys():
        returnvalue = nickdict[dictkey]
    else:
        nickdict[dictkey] = 0
        returnvalue = 0

    return returnvalue


# set a value
def set_user_dict(bot, dynamic_class, nick, dictkey, value):
    currentvalue = get_user_dict(bot, dynamic_class, nick, dictkey)
    nickdict = eval('dynamic_class.userdb.' + nick)
    nickdict[dictkey] = value


# reset a value
def reset_user_dict(bot, dynamic_class, nick, dictkey):
    currentvalue = get_user_dict(bot, dynamic_class, nick, dictkey)
    nickdict = eval('dynamic_class.userdb.' + nick)
    if dictkey in nickdict:
        del nickdict[dictkey]


# add or subtract from current value
def adjust_user_dict(bot, dynamic_class, nick, dictkey, value):
    oldvalue = get_user_dict(bot, dynamic_class, nick, dictkey)
    if not str(oldvalue).isdigit():
        oldvalue = 0
    nickdict = eval('dynamic_class.userdb.' + nick)
    nickdict[dictkey] = oldvalue + value


# Save all database users in list
def save_user_dicts(bot, dynamic_class):

    # check that db list is there
    if not hasattr(dynamic_class, 'userdb'):
        dynamic_class.userdb = class_create('userdblist')
    if not hasattr(dynamic_class.userdb, 'list'):
        dynamic_class.userdb.list = []

    for nick in dynamic_class.userdb.list:
        if not hasattr(dynamic_class.userdb, nick):
            nickdict = dict()
        else:
            nickdict = eval('dynamic_class.userdb.' + nick)
        set_database_value(bot, nick, dynamic_class.default, nickdict)


# add or subtract from current value
def adjust_user_dict_array(bot, dynamic_class, nick, dictkey, entries, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
    oldvalue = get_user_dict(bot, dynamic_class, nick, dictkey)
    nickdict = eval('dynamic_class.userdb.' + nick)
    if not isinstance(oldvalue, list):
        oldvalue = []
    for x in entries:
        if adjustmentdirection == 'add':
            if x not in oldvalue:
                oldvalue.append(x)
        elif adjustmentdirection == 'del':
            if x in oldvalue:
                oldvalue.remove(x)
    nickdict[dictkey] = oldvalue


def database_initialize(bot, nick, array, database):
    databasekey = str(database)
    existingarray = get_database_value(bot, bot.nick, databasekey)
    if not existingarray:
        arraycount = (len(array) - 1)
        i = 0
        while (i <= arraycount):
            inputstring = array[i]
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
            i = i + 1


"""
# Sayings Functions
"""


def sayingsmodule(bot, databasekey, inputarray, thingtodo):
    """Handle the creation and manipulation of modules that return sayings."""
    # Usage: message = sayingsmodule(bot, 'techsupport', triggerargsarray, 'random')
    # Usage: message = sayingsmodule(bot, 'techsupport', triggerargsarray, 'add')
    response = "Something went wrong. Oops."
    inputstring = spicemanip.main(inputarray, '2+')
    existingarray = get_database_value(bot, bot.nick, databasekey) or []
    if thingtodo == "initialise":
        database_initialize(bot, bot.nick, inputarray, databasekey)
    elif thingtodo == "add":
        if inputstring not in existingarray:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
            response = "Added to database."
        else:
            response = "That is already in the database."
    elif thingtodo == "remove" or thingtodo == 'del':
        if inputstring not in existingarray:
            response = "That was not found in the database."
        else:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'del')
            response = "Removed from database."
    elif thingtodo == "count":
        messagecount = len(existingarray)
        response = "I'm seeing " + str(messagecount) + " responses in the database."
    elif thingtodo == "last":
        response = spicemanip.main(existingarray, "last") or "I appear to have nothing for that."
    else:
        response = spicemanip.main(existingarray, "random") or ''
        if response == '':
            response = "I'm afraid I couldn't find an entry for that."
    return response


def sayingscheck(bot, databasekey):
    """Check that there are responses for the given key."""
    saying_entries = get_database_value(bot, bot.nick, databasekey) or []
    saying_entrycount = len(saying_entries)
    if saying_entrycount != 0:
        return True
    else:
        return False


"""
Get line from raw text site.
"""


def randomline(bot, address):
    """Retrieve random line from given raw file."""
    htmlfile = urllib.urlopen(address)
    lines = htmlfile.read().splitlines()
    myline = random.choice(lines)
    if not myline or myline == '\n':
        myline = randomline()
    return myline


"""
On Screen Text
"""


def osd(bot, recipients, text_type, messages):

    if not isinstance(messages, list):
        messages = [messages]

    if not isinstance(recipients, list):
        recipients = [recipients]
    recipients = ','.join(str(x) for x in recipients)

    messages_refactor = ['']
    for message in messages:
        chunknum = 0
        chunks = message.split()
        for chunk in chunks:
            if not chunknum:
                if messages_refactor[-1] == '':
                    if len(chunk) <= 420:
                        messages_refactor[-1] = chunk
                    else:
                        chunksplit = map(''.join, zip(*[iter(chunk)]*420))
                        messages_refactor.extend(chunksplit)
                elif len(messages_refactor[-1] + "   " + chunk) <= 420:
                    messages_refactor[-1] = messages_refactor[-1] + "   " + chunk
                else:
                    if len(chunk) <= 420:
                        messages_refactor.append(chunk)
                    else:
                        chunksplit = map(''.join, zip(*[iter(chunk)]*420))
                        messages_refactor.extend(chunksplit)
            else:
                if len(messages_refactor[-1] + " " + chunk) <= 420:
                    messages_refactor[-1] = messages_refactor[-1] + " " + chunk
                else:
                    if len(chunk) <= 420:
                        messages_refactor.append(chunk)
                    else:
                        chunksplit = map(''.join, zip(*[iter(chunk)]*420))
                        messages_refactor.extend(chunksplit)
            chunknum += 1

    for combinedline in messages_refactor:
        if text_type == 'action':
            bot.action(combinedline, recipients)
            text_type = 'say'
        elif text_type == 'notice':
            bot.notice(combinedline, recipients)
        else:
            bot.say(combinedline, recipients)


"""
Array/List/String Manipulation
"""


# Legacy
def get_trigger_arg(bot, inputs, outputtask, output_type='default'):
    return spicemanip.main(inputs, outputtask, output_type)


def array_arrangesort(bot, sortbyarray, arrayb):
    sortbyarray, arrayb = (list(x) for x in zip(*sorted(zip(sortbyarray, arrayb), key=itemgetter(0))))
    return sortbyarray, arrayb


"""
# Empty Classes
"""


def class_create(classname):
    compiletext = """
        def __init__(self):
            self.default = str(self.__class__.__name__)
        def __repr__(self):
            return repr(self.default)
        def __str__(self):
            return str(self.default)
        def __iter__(self):
            return str(self.default)
        pass
        """
    exec(compile("class class_" + str(classname) + ": " + compiletext, "", "exec"))
    newclass = eval('class_'+classname+"()")
    return newclass


"""
# File functions
"""


def txtFileCount(path):
    with open(path) as f:
        line_count = 0
        for line in f:
            line_count += 1

    return line_count


def fileLine(path, number):
    maxLines = txtFileCount(path)
    if number < 0:
        number = 1
    if number > maxLines:
        number = 1
    file = open(path, "r")
    i = 1
    while i <= number:
        line = file.readline()
        i = i + 1
    return line


def randomFileLine(path):
    maxLines = txtFileCount(path)
    rand = random.randint(1, maxLines)
    file = open(path, "r")
    i = 1
    while i <= rand:
        line = file.readline()
        i = i + 1
    return line


"""
Other Python Functions
"""


def unique_id_create(bot):
    unique_id = 0
    while unique_id in bot.memory['rpg']['message_display']["used_ids"]:
        unique_id = uuid.uuid4()
    bot.memory['rpg']['message_display']["used_ids"].append(unique_id)
    return unique_id


def bytecount(s):
    return len(s.encode('utf-8'))
