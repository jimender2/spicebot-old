#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.module import commands, nickname_commands, event, rule, OP, ADMIN, VOICE

# imports for system and OS access, directories
import os
import sys

# Additional imports
import datetime
import time
import re

# Opening and reading config files
import ConfigParser

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

"""
Variables
"""


osd_limit = 420  # Ammount of text allowed to display per line


"""
Bot Dictionary
"""

bot_dict = {
                # Some values don't get saved to the database, but stay in memory
                "tempvals": {

                            # Indicate if we need to pull the dict from the database
                            "dict_loaded": False,

                            # Time The Bot started last
                            "uptime": None,

                            # Configs directory
                            "config_dir": None,

                            # Loaded configs
                            "commands_loaded": [],

                            # server the bot is connected to
                            "server": False,
                            "servername": False,

                            # Channels
                            "channels_list": {},

                            # Current Users
                            "all_current_users": [],

                            # offline users
                            "offline_users": [],

                            # Bots
                            "bots_list": {},

                            # End of Temp Vals
                            },

                # Static content
                "static": {},

                # Users lists
                "users": {
                            "users_all": {},
                            },

                }


def botdict_open(bot):

    if "botdict_loaded" in bot.memory:
        return
    bot.memory["botdict"] = botdict_setup_open(bot)

    if not bot.memory["botdict"]["tempvals"]["uptime"]:
        bot.memory["botdict"]["tempvals"]["uptime"] = datetime.datetime.utcnow()

    # Server connected to, default assumes ZNC bouncer configuration
    # this can be tweaked below
    botdict_setup_server(bot)

    # Channel Listing
    botdict_setup_channels(bot)

    # Bot configs
    botdict_setup_bots(bot)

    # use this to prevent bot usage if the above isn't done loading
    bot.memory["botdict_loaded"] = True


def botdict_setup_open(bot):

    # open global dict
    global bot_dict
    botdict = bot_dict

    # don't pull from database if already open
    if not botdict["tempvals"]["dict_loaded"]:
        opendict = botdict.copy()
        dbbotdict = get_database_value(bot, bot.nick, 'bot_dict') or dict()
        opendict = merge_botdict(opendict, dbbotdict)
        botdict.update(opendict)
        botdict["tempvals"]['dict_loaded'] = True
    return botdict


def merge_botdict(a, b, path=None):
    "merges b into a"
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_botdict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def botdict_save(bot):
    botdict_open(bot)

    # copy dict to not overwrite
    savedict = bot.memory["botdict"].copy()

    # Values to not save to database
    savedict_del = ['tempvals', 'static']
    for dontsave in savedict_del:
        if dontsave in savedict.keys():
            del savedict[dontsave]

    # save to database
    set_database_value(bot, bot.nick, 'bot_dict', savedict)


"""
Bot Servers
"""


def botdict_setup_server(bot):

    # if host is set in the config without a bouncer, uncomment the next two lines:
    # bot.memory["botdict"]["tempvals"]['server'] = bot.config.core.host
    # return

    # The server the bot is connected to. Sopel limit is one
    # this detects the use of an IRC bouncer like ZNC
    # This is a custom function for this bot's connection
    if not bot.memory["botdict"]["tempvals"]['server']:
        if ipv4detect(bot, bot.config.core.host):
            servername = str(bot.config.core.user.split("/", 1)[1])
            if servername == 'SpiceBot':
                server = 'irc.spicebot.net'
            elif servername == 'Freenode':
                server = 'irc.freenode.net'
            else:
                server = bot.config.core.host
        else:
            server = bot.config.core.host
        bot.memory["botdict"]["tempvals"]['server'] = server

    if not bot.memory["botdict"]["tempvals"]['servername']:
        if ipv4detect(bot, bot.config.core.host):
            servername = str(bot.config.core.user.split("/", 1)[1])
            if servername not in tuple(["SpiceBot", "Freenode"]):
                servername = bot.config.core.host
        else:
            servername = bot.config.core.host
        bot.memory["botdict"]["tempvals"]['servername'] = servername


def ipv4detect(bot, hostIP):
    pat = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
    test = pat.match(hostIP)
    return test


"""
Bot Channels
"""


def botdict_setup_channels(bot):

    # All channels the bot is in
    if bot.memory["botdict"]["tempvals"]['channels_list'].keys() == []:
        for channel in bot.channels:
            if channel not in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
                bot.memory["botdict"]["tempvals"]['channels_list'][channel] = dict()


"""
Users
"""


def botdict_setup_bots(bot):

    if not bot.memory["botdict"]["tempvals"]['config_dir']:
        bot.memory["botdict"]["tempvals"]['config_dir'] = str("/home/spicebot/.sopel/" + bot.nick + "/System-Files/Configs/" + bot.memory["botdict"]["tempvals"]['servername'] + "/")

    # all bot configs present
    if bot.memory["botdict"]["tempvals"]['bots_list'].keys() == []:
        for filename in os.listdir(bot.memory["botdict"]["tempvals"]['config_dir']):
            filenameminuscfg = str(filename).replace(".cfg", "")
            if filenameminuscfg not in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                bot.memory["botdict"]["tempvals"]['bots_list'][filenameminuscfg] = dict()

    for botconf in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
        if bot.memory["botdict"]["tempvals"]['bots_list'][botconf] == dict():
            if 'name' not in bot.memory["botdict"]["tempvals"]['bots_list'][botconf].keys():
                bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['name'] = botconf
            if 'directory' not in bot.memory["botdict"]["tempvals"]['bots_list'][botconf].keys():
                joindpath = os.path.join("/home/spicebot/.sopel/", botconf)
                if os.path.isdir(joindpath):
                    bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['directory'] = joindpath
                else:
                    bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['directory'] = None
            if 'config_file' not in bot.memory["botdict"]["tempvals"]['bots_list'][botconf].keys():
                bot.memory["botdict"]["tempvals"]['config_file'] = str(bot.memory["botdict"]["tempvals"]['config_dir'] + str(botconf) + ".cfg")
            if 'configuration' not in bot.memory["botdict"]["tempvals"]['bots_list'][botconf].keys():
                bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['configuration'] = dict()
                # Read configuration
                config = ConfigParser.ConfigParser()
                config.read(bot.memory["botdict"]["tempvals"]['config_file'])
                for each_section in config.sections():
                    if each_section not in bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['configuration'].keys():
                        bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['configuration'][each_section] = dict()
                        for (each_key, each_val) in config.items(each_section):
                            if each_key not in bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['configuration'][each_section].keys():
                                bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['configuration'][each_section][each_key] = each_val


def botdict_setup_users(bot):

    for channelcheck in bot.memory["botdict"]["tempvals"]['channels_list'].keys():

        if 'chanops' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanops'] = []

        if 'chanhalfops' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanhalfops'] = []

        if 'chanvoices' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanvoices'] = []

        if 'current_users' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['current_users'] = []

        for user in bot.privileges[channelcheck].keys():

            if bot.privileges[channelcheck][user] == OP:
                if user not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanops']:
                    bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanops'].append(user)

            elif bot.privileges[channelcheck][user] == HALFOP:
                if user not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanhalfops']:
                    bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanhalfops'].append(user)

            elif bot.privileges[channelcheck][user] == VOICE:
                if user not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanvoices']:
                    bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanvoices'].append(user)

            if user not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['current_users']:
                bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['current_users'].append(user)

        for user in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['current_users']:
            if user not in bot.memory["botdict"]["users"]['users_all'].keys():
                bot.memory["botdict"]["users"]['users_all'][user] = dict()
            if user not in bot.memory["botdict"]["tempvals"]['all_current_users']:
                bot.memory["botdict"]["tempvals"]['all_current_users'].append(user)

    for user in bot.memory["botdict"]["users"]['users_all'].keys():
        if user not in bot.memory["botdict"]["tempvals"]['all_current_users']:
            if user not in bot.memory["botdict"]["tempvals"]['offline_users']:
                bot.memory["botdict"]["tempvals"]['offline_users'].append(user)


def nick_actual(bot, nick):
    nick_actual = nick
    for u in bot.memory["botdict"]["users"]['users_all'].keys():
        if u.lower() == str(nick).lower():
            nick_actual = u
    return nick_actual


"""
Small Functions
"""


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


"""
Database
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
On Screen Text
"""


def osd(bot, target_array, text_type_array, text_array):

    # if text_array is a string, make it an array
    textarraycomplete = []
    if not isinstance(text_array, list):
        textarraycomplete.append(text_array)
    else:
        for x in text_array:
            textarraycomplete.append(x)

    # if target_array is a string, make it an array
    texttargetarray = []
    if not isinstance(target_array, list):
        if not str(target_array).startswith("#"):
            target_array = nick_actual(bot, str(target_array))
        texttargetarray.append(target_array)
    else:
        for target in target_array:
            if not str(target).startswith("#"):
                target = nick_actual(bot, str(target))
            texttargetarray.append(target)

    # Handling for text_type
    texttypearray = []
    if not isinstance(text_type_array, list):
        for i in range(len(texttargetarray)):
            texttypearray.append(str(text_type_array))
    else:
        for x in text_type_array:
            texttypearray.append(str(x))
    text_array_common = max(((item, texttypearray.count(item)) for item in set(texttypearray)), key=lambda a: a[1])[0]

    # make sure len() equals
    if len(texttargetarray) > len(texttypearray):
        while len(texttargetarray) > len(texttypearray):
            texttypearray.append(text_array_common)
    elif len(texttargetarray) < len(texttypearray):
        while len(texttargetarray) < len(texttypearray):
            texttargetarray.append('osd_error_handle')

    # Rebuild the text array to ensure string lengths

    for target, text_type in zip(texttargetarray, texttypearray):

        if target == 'osd_error_handle':
            dont_say_it = 1
        else:

            # Text array
            temptextarray = []

            # Notice handling
            if text_type == 'notice':
                temptextarray.insert(0, target + ", ")
                # temptextarray.append(target + ", ")
            for part in textarraycomplete:
                temptextarray.append(part)

            # 'say' can equal 'priv'
            if text_type == 'say' and not str(target).startswith("#"):
                text_type = 'priv'

            # Make sure no individual string ins longer than it needs to be
            currentstring = ''
            texttargetarray = []
            for textstring in temptextarray:
                if len(textstring) > osd_limit:
                    chunks = textstring.split()
                    for chunk in chunks:
                        if currentstring == '':
                            currentstring = chunk
                        else:
                            tempstring = str(currentstring + " " + chunk)
                            if len(tempstring) <= osd_limit:
                                currentstring = tempstring
                            else:
                                texttargetarray.append(currentstring)
                                currentstring = chunk
                    if currentstring != '':
                        texttargetarray.append(currentstring)
                else:
                    texttargetarray.append(textstring)

            # Split text to display nicely
            combinedtextarray = []
            currentstring = ''
            for textstring in texttargetarray:
                if currentstring == '':
                    currentstring = textstring
                elif len(textstring) > osd_limit:
                    if currentstring != '':
                        combinedtextarray.append(currentstring)
                        currentstring = ''
                    combinedtextarray.append(textstring)
                else:
                    tempstring = currentstring + "   " + textstring
                    if len(tempstring) <= osd_limit:
                        currentstring = tempstring
                    else:
                        combinedtextarray.append(currentstring)
                        currentstring = textstring
            if currentstring != '':
                combinedtextarray.append(currentstring)

            # display
            textparts = len(combinedtextarray)
            textpartsleft = textparts
            for combinedline in combinedtextarray:
                if text_type == 'action' and textparts == textpartsleft:
                    bot.action(combinedline, target)
                elif str(target).startswith("#"):
                    bot.msg(target, combinedline)
                elif text_type == 'notice' or text_type == 'priv':
                    bot.notice(combinedline, target)
                elif text_type == 'say':
                    bot.say(combinedline)
                else:
                    bot.say(combinedline)
                textpartsleft = textpartsleft - 1


"""
Array/List/String Manipulation
"""


# Hub
def spicemanip(bot, inputs, outputtask, output_type='default'):

    # TODO 'this*that' or '1*that' replace either all strings matching, or an index value
    # TODO reverse sort z.sort(reverse = True)
    # list.extend adds lists to eachother

    mainoutputtask, suboutputtask = None, None

    # Input needs to be a list, but don't split a word into letters
    if not inputs:
        inputs = []
    if not isinstance(inputs, list):
        inputs = list(inputs.split(" "))
        inputs = [x for x in inputs if x and x not in ['', ' ']]
        inputs = [inputspart.strip() for inputspart in inputs]

    # Create return
    if outputtask == 'create':
        return inputs

    # Make temparray to preserve original order
    temparray = []
    for inputpart in inputs:
        temparray.append(inputpart)
    inputs = temparray

    # Convert outputtask to standard
    if outputtask in [0, 'complete']:
        outputtask = 'string'
    elif outputtask == 'index':
        mainoutputtask = inputs[1]
        suboutputtask = inputs[2]
        inputs = inputs[0]
    elif str(outputtask).isdigit():
        mainoutputtask, outputtask = int(outputtask), 'number'
    elif "^" in str(outputtask):
        mainoutputtask = str(outputtask).split("^", 1)[0]
        suboutputtask = str(outputtask).split("^", 1)[1]
        outputtask = 'rangebetween'
        if int(suboutputtask) < int(mainoutputtask):
            mainoutputtask, suboutputtask = suboutputtask, mainoutputtask
    elif str(outputtask).startswith("split_"):
        mainoutputtask = str(outputtask).replace("split_", "")
        outputtask = 'split'
    elif str(outputtask).endswith(tuple(["!", "+", "-", "<", ">"])):
        mainoutputtask = str(outputtask)
        if str(outputtask).endswith("!"):
            outputtask = 'exclude'
        if str(outputtask).endswith("+"):
            outputtask = 'incrange_plus'
        if str(outputtask).endswith("-"):
            outputtask = 'incrange_minus'
        if str(outputtask).endswith(">"):
            outputtask = 'excrange_plus'
        if str(outputtask).endswith("<"):
            outputtask = 'excrange_minus'
        for r in (("!", ""), ("+", ""), ("-", ""), ("<", ""), (">", "")):
            mainoutputtask = mainoutputtask.replace(*r)

    if outputtask == 'string':
        returnvalue = inputs
    else:
        try:
            returnvalue = eval('spicemanip_' + outputtask + '(bot, inputs, outputtask, mainoutputtask, suboutputtask)')
        except NameError:
            returnvalue = ''

    # default return if not specified
    if output_type == 'default':
        if outputtask in [
                            'string', 'number', 'rangebetween', 'exclude', 'random',
                            'incrange_plus', 'incrange_minus', 'excrange_plus', 'excrange_minus'
                            ]:
            output_type = 'string'
        elif outputtask in ['count']:
            output_type = 'dict'

    # verify output is correct
    if output_type == 'string':
        if isinstance(returnvalue, list):
            returnvalue = ' '.join(returnvalue)
    elif output_type in ['list', 'array']:
        if not isinstance(returnvalue, list):
            returnvalue = list(returnvalue.split(" "))
            returnvalue = [x for x in returnvalue if x and x not in ['', ' ']]
            returnvalue = [inputspart.strip() for inputspart in returnvalue]
    return returnvalue


# compare 2 lists, based on the location of an index item, passthrough needs to be [indexitem, arraytoindex, arraytocompare]
def spicemanip_index(bot, indexitem, outputtask, arraytoindex, arraytocompare):
    item = ''
    for x, y in zip(arraytoindex, arraytocompare):
        if x == indexitem:
            item = y
    return item


# split list by string
def spicemanip_split(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    split_array = []
    restring = ' '.join(inputs)
    if mainoutputtask not in inputs:
        split_array = [restring]
    else:
        split_array = restring.split(mainoutputtask)
    split_array = [x for x in split_array if x and x not in ['', ' ']]
    split_array = [inputspart.strip() for inputspart in split_array]
    if split_array == []:
        split_array = [[]]
    return split_array


# dedupe list
def spicemanip_dedupe(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    newlist = []
    for inputspart in inputs:
        if inputspart not in newlist:
            newlist.append(inputspart)
    return newlist


# Sort list
def spicemanip_sort(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    return sorted(inputs)


# reverse sort list
def spicemanip_rsort(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    return sorted(inputs)[::-1]


# count items in list, return dictionary
def spicemanip_count(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    returndict = dict()
    if inputs == []:
        return returndict
    uniqueinputitems, uniquecount = [], []
    for inputspart in inputs:
        if inputspart not in uniqueinputitems:
            uniqueinputitems.append(inputspart)
    for uniqueinputspart in uniqueinputitems:
        count = 0
        for ele in inputs:
            if (ele == uniqueinputspart):
                count += 1
        uniquecount.append(count)
    for inputsitem, unumber in zip(uniqueinputitems, uniquecount):
        returndict[inputsitem] = unumber
    return returndict


# random item from list
def spicemanip_random(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    randomselectlist = []
    for temppart in inputs:
        randomselectlist.append(temppart)
    while len(randomselectlist) > 1:
        random.shuffle(randomselectlist)
        randomselect = randomselectlist[random.randint(0, len(randomselectlist) - 1)]
        randomselectlist.remove(randomselect)
    randomselect = randomselectlist[0]
    return randomselect


# remove random item from list
def spicemanip_exrandom(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return []
    randremove = spicemanip_random(bot, inputs, outputtask, mainoutputtask, suboutputtask)
    inputs.remove(randremove)
    return inputs


# Convert list into lowercase
def spicemanip_lower(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return [inputspart.lower() for inputspart in inputs]


# Convert list to uppercase
def spicemanip_upper(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return [inputspart.upper() for inputspart in inputs]


# Convert list to uppercase
def spicemanip_title(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return [inputspart.title() for inputspart in inputs]


# Reverse List Order
def spicemanip_reverse(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return []
    return inputs[::-1]


# comma seperated list
def spicemanip_list(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return ', '.join(str(x) for x in inputs)


# comma seperated list with and
def spicemanip_andlist(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    if len(inputs) < 2:
        return ' '.join(inputs)
    lastentry = str("and " + str(inputs[len(inputs) - 1]))
    del inputs[-1]
    inputs.append(lastentry)
    if len(inputs) == 2:
        return ' '.join(inputs)
    return ', '.join(str(x) for x in inputs)


# comma seperated list with or
def spicemanip_orlist(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    if len(inputs) < 2:
        return ' '.join(inputs)
    lastentry = str("or " + str(inputs[len(inputs) - 1]))
    del inputs[-1]
    inputs.append(lastentry)
    if len(inputs) == 2:
        return ' '.join(inputs)
    return ', '.join(str(x) for x in inputs)


# exclude number
def spicemanip_exclude(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    del inputs[int(mainoutputtask) - 1]
    return ' '.join(inputs)


# Convert list to string
def spicemanip_string(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return ' '.join(inputs)


# Get number item from list
def spicemanip_number(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    elif len(inputs) == 1:
        return inputs[0]
    elif int(mainoutputtask) > len(inputs) or int(mainoutputtask) < 0:
        return ''
    else:
        return inputs[int(mainoutputtask) - 1]


# Get Last item from list
def spicemanip_last(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return inputs[len(inputs) - 1]


# range between items in list
def spicemanip_rangebetween(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    if not str(mainoutputtask).isdigit() or not str(suboutputtask).isdigit():
        return ''
    mainoutputtask, suboutputtask = int(mainoutputtask), int(suboutputtask)
    if suboutputtask == mainoutputtask:
        return spicemanip_number(bot, inputs, outputtask, mainoutputtask, suboutputtask)
    if suboutputtask < mainoutputtask:
        return []
    if mainoutputtask < 0:
        mainoutputtask = 1
    if suboutputtask > len(inputs):
        suboutputtask = len(inputs)
    newlist = []
    for i in range(mainoutputtask, suboutputtask + 1):
        newlist.append(str(spicemanip_number(bot, inputs, outputtask, i, suboutputtask)))
    if newlist == []:
        return ''
    return ' '.join(newlist)


# Forward Range includes index number
def spicemanip_incrange_plus(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return spicemanip_rangebetween(bot, inputs, outputtask, int(mainoutputtask), len(inputs))


# Reverse Range includes index number
def spicemanip_incrange_minus(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return spicemanip_rangebetween(bot, inputs, outputtask, 1, int(mainoutputtask))


# Forward Range excludes index number
def spicemanip_excrange_plus(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return spicemanip_rangebetween(bot, inputs, outputtask, int(mainoutputtask) + 1, len(inputs))


# Reverse Range excludes index number
def spicemanip_excrange_minus(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return spicemanip_rangebetween(bot, inputs, outputtask, 1, int(mainoutputtask) - 1)


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
