#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
# sopel imports
import sopel.module
from sopel.module import commands, nickname_commands, rule, priority, example, OP, ADMIN, VOICE, event, rule
from sopel.formatting import bold
import sopel
from sopel import module, tools, formatting
from .Global_Vars import *


"""
Idea, use exec to dynamically import the subcommands?
"""


# Base command
@sopel.module.commands('rpg')
@sopel.module.thread(True)
def rpg_trigger_main(bot, trigger):
    rpg = class_create('main')
    triggerargsarray = get_trigger_arg(bot, trigger.group(2), 'create')
    execute_main(bot, trigger, triggerargsarray, rpg)


# respond to alternate start for command
@module.rule('^(?:rpg)\s+?.*')
@module.rule('^(?:!rpg)\s+?.*')
@module.rule('^(?:,rpg)\s+?.*')
@sopel.module.thread(True)
def rpg_trigger_precede(bot, trigger):
    rpg = class_create('main')
    triggerargsarray = get_trigger_arg(bot, trigger.group(0), 'create')
    triggerargsarray = get_trigger_arg(bot, triggerargsarray, '2+')
    triggerargsarray = get_trigger_arg(bot, triggerargsarray, 'create')
    execute_main(bot, trigger, triggerargsarray, rpg)


def execute_main(bot, trigger, triggerargsarray, rpg):

    # Channel Listing
    rpg = rpg_command_channels(bot,rpg,trigger)

    # Bacic User List
    rpg = rpg_command_users(bot,rpg)

    # No Empty Commands
    if triggerargsarray == []:
        osd(bot, trigger.nick, 'notice', "No Command issued.")
        return
    rpg.command_full_complete = get_trigger_arg(bot, triggerargsarray, 0)

    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    rpg.multi_com_list = []

    # Build array of commands used
    if not [x for x in triggerargsarray if x == "&&"]:
        rpg.multi_com_list.append(rpg.command_full_complete)
    else:
        command_full_split = rpg.command_full_complete.split("&&")
        for command_split in command_full_split:
            rpg.multi_com_list.append(command_split)

    # instigator
    instigator = class_create('instigator')
    instigator.default = trigger.nick
    rpg.instigator = trigger.nick

    # Cycle through command array
    for command_split_partial in rpg.multi_com_list:
        rpg.triggerargsarray = get_trigger_arg(bot, command_split_partial, 'create')

        # Admin only
        rpg.admin = 0
        if [x for x in rpg.triggerargsarray if x == "-a"]:
            rpg.triggerargsarray.remove("-a")
            if trigger.admin:
                rpg.admin = 1

        # Split commands to pass
        rpg.command_full = get_trigger_arg(bot, rpg.triggerargsarray, 0)
        rpg.command_main = get_trigger_arg(bot, rpg.triggerargsarray, 1).lower()

        # Run command process
        command_process(bot, trigger, rpg, instigator)


def command_process(bot, trigger, rpg, instigator):

    # Handle rog commands
    if rpg.command_main not in rpg_valid_commands:
        return osd(bot, rpg.instigator, 'notice', "You have not specified a valid command.")

    command_function_run = str('rpg_command_main_' + rpg.command_main + '(bot, rpg, instigator)')
    try:
        eval(command_function_run)
    except NameError:
        return osd(bot, rpg.instigator, 'notice', "That is a valid command, however the functionality has not been developed yet.")


def rpg_command_main_admin(bot,rpg):
    bot.say("wip")


"""
Channels
"""


def rpg_command_channels(bot,rpg,trigger):

    # current Channels
    rpg.channel_current = trigger.sender

    # determine the type of channel
    if not rpg.channel_current.startswith("#"):
        rpg.channel_priv = 1
        rpg.channel_real = 0
    else:
        rpg.channel_priv = 0
        rpg.channel_real = 1

    # All channels the bot is in
    rpg.channels_list = []
    for channel in bot.channels:
        rpg.channels_list.append(channel)

    # Game Enabled
    rpg.channels_enabled = get_database_value(bot, 'rpg_game_records', 'gameenabled') or []

    # Development mode
    rpg.channels_devmode = get_database_value(bot, 'rpg_game_records', 'devenabled') or []
    rpg.dev_bypass = 0
    if rpg.channel_current.lower() in [x.lower() for x in rpg.channels_devmode]:
        rpg.dev_bypass = 1
    return rpg


"""
Users
"""


def rpg_command_users(bot,rpg):
    rpg.opadmin,rpg.owner,rpg.chanops,rpg.chanvoice,rpg.botadmins,rpg.users_current = [],[],[],[],[],[]

    for user in bot.users:
        rpg.users_current.append(str(user))
    adjust_database_array(bot, 'channel', rpg.users_current, 'users_all', 'add')
    rpg.users_all = get_database_value(bot, 'channel', 'users_all') or []

    for user in rpg.users_current:

        if user in bot.config.core.owner:
            rpg.owner.append(user)

        if user in bot.config.core.admins:
            rpg.botadmins.append(user)
            rpg.opadmin.append(user)

        for channelcheck in bot.channels:
            try:
                if bot.privileges[channelcheck][user] == OP:
                    rpg.chanops.append(user)
                    rpg.opadmin.append(user)
            except KeyError:
                dummyvar = 1
            try:
                if bot.privileges[channelcheck][user] == VOICE:
                    rpg.chanvoice.append(user)
            except KeyError:
                dummyvar = 1

    return rpg


"""
On Screen Text
"""


def osd(bot, target_array, text_type, text_array):

    # if text_array is a string, make it an array
    textarraycomplete = []
    if not isinstance(text_array, list):
        textarraycomplete.append(str(text_array))
    else:
        for x in text_array:
            textarraycomplete.append(str(x))

    # if target_array is a string, make it an array
    texttargetarray = []
    if not isinstance(target_array, list):
        if not str(target_array).startswith("#"):
            target_array = nick_actual(bot,str(target_array))
        texttargetarray.append(target_array)
    else:
        for target in target_array:
            if not str(target).startswith("#"):
                target = nick_actual(bot,str(target))
            texttargetarray.append(target)

    # Make sure we don't cross over IRC limits
    for target in texttargetarray:
        temptextarray = []
        if text_type == 'notice':
            temptextarray.append(target + ", ")
        for part in textarraycomplete:
            temptextarray.append(part)

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
                tempstring = str(currentstring + "   " + textstring)
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
                bot.action(combinedline,target)
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
How to Display Nicks
"""


# Outputs Nicks with correct capitalization
def nick_actual(bot,nick):
    actualnick = nick
    for u in bot.users:
        if u.lower() == actualnick.lower():
            actualnick = u
            continue
    return actualnick


"""
Array/List/String Manipulation
"""


# Hub
def get_trigger_arg(bot, inputs, outputtask):
    # Create
    if outputtask == 'create':
        return create_array(bot, inputs)
    # reverse
    if outputtask == 'reverse':
        return reverse_array(bot, inputs)
    # Comma Seperated List
    if outputtask == 'list':
        return list_array(bot, inputs)
    if outputtask == 'random':
        return random_array(bot, inputs)
    # Last element
    if outputtask == 'last':
        return last_array(bot, inputs)
    # Complete String
    if outputtask == 0 or outputtask == 'complete' or outputtask == 'string':
        return string_array(bot, inputs)
    # Number
    if str(outputtask).isdigit():
        return number_array(bot, inputs, outputtask)
    # Exlude from array
    if str(outputtask).endswith("!"):
        return excludefrom_array(bot, inputs, outputtask)
    # Inclusive range starting at
    if str(outputtask).endswith("+"):
        return incrange_plus_array(bot, inputs, outputtask)
    # Inclusive range ending at
    if str(outputtask).endswith("-"):
        return incrange_minus_array(bot, inputs, outputtask)
    # Exclusive range starting at
    if str(outputtask).endswith(">"):
        return excrange_plus_array(bot, inputs, outputtask)
    # Exclusive range ending at
    if str(outputtask).endswith("<"):
        return excrange_minus_array(bot, inputs, outputtask)
    # Range Between Numbers
    if "^" in str(outputtask):
        return rangebetween_array(bot, inputs, outputtask)
    string = ''
    return string


# Convert String to array
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


# Convert Array to String
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


# output reverse order
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


# Comma Seperated List
def list_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    for x in inputs:
        if string != '':
            string = str(str(string) + ", " + str(x))
        else:
            string = str(x)
    return string


# Random element
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
    string = str(temparray[randomselected])
    return string


# Last element
def last_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    string = inputs[len(inputs)-1]
    return string


# select a number
def number_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if str(number).isdigit():
        numberadjust = int(number) - 1
        if numberadjust < len(inputs) and numberadjust >= 0:
            number = int(number) - 1
            string = inputs[number]
    return string


# range
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
        return string
    for i in range(int(rangea),int(rangeb) + 1):
        arg = number_array(bot, inputs, i)
        if string != '':
            string = str(string + " " + arg)
        else:
            string = str(arg)
    return string


# exclude a number
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


# range between
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


# inclusive forward
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


# inclusive reverse
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


# excluding forward
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


# excluding reverse
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


def array_compare(bot, indexitem, arraytoindex, arraytocompare):
    item = ''
    for x, y in zip(arraytoindex, arraytocompare):
        if x == indexitem:
            item = y
    return item


def array_arrangesort(bot, sortbyarray, arrayb):
    sortbyarray, arrayb = (list(x) for x in zip(*sorted(zip(sortbyarray, arrayb),key=itemgetter(0))))
    return sortbyarray, arrayb


"""
Database
"""


# Get a value
def get_database_value(bot, nick, databasekey):
    databasecolumn = str('rpg_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value


# set a value
def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('rpg_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)


# set a value to None
def reset_database_value(bot, nick, databasekey):
    databasecolumn = str('rpg_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, None)


# add or subtract from current value
def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey) or 0
    databasecolumn = str('rpg_' + databasekey)
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


"""
Dynamic Classes
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
        def __unicode__(self):
            return str(u+self.default)
        def lower(self):
            return str(self.default).lower()
        pass
        """
    exec(compile("class class_" + str(classname) + ": " + compiletext,"","exec"))
    newclass = eval('class_'+classname+"()")
    return newclass
