#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
from random import randint
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# author jimender2

databasekey = 'lf'

defaultoptions = [
            "test"]


hardcoded_not_in_this_chan = ["#spiceworks", "##spicebottest", "#spicebottest"]


@sopel.module.commands('lh', 'lifehack', 'lifehacks')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'lh')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Check to see if there are Lifehacks and retrieve one."""
    command = spicemanip(bot, triggerargsarray, 1) or 'get'
    if not sayingscheck(bot, databasekey) and command != "add":
        sayingsmodule(bot, databasekey, defaultoptions, 'initialise')
    message = sayingsmodule(bot, databasekey, triggerargsarray, command)
    rando = random.randint(1,10000)
    rand = str(rando)
    osd(bot, trigger.sender, 'say', ["[Lifehack Number", rand,"]", message, "[Lifehack]"])


@sopel.module.interval(60)
def lifehack(bot):
    """Get and share random lifehack at random intervals."""
    now = time.time()

    last_timesince = time_since(bot, bot.nick, "lh_last_time") or 0
    next_timeout = get_database_value(bot, bot.nick, "lf_next_timeout") or 0
    if last_timesince <= next_timeout:
        return

    # set time to now
    set_database_value(bot, bot.nick, "lh_last_time", now)

    # how long until next event
    next_timeout = randint(1200, 7200)
    set_database_value(bot, bot.nick, "lh_next_timeout", next_timeout)

    message = sayingsmodule(bot, databasekey, defaultoptions, 'get') or "Click all the links"

    for channel in bot.channels:
        if channel not in hardcoded_not_in_this_chan:
            channelmodulesarray = get_database_value(bot, channel, 'modules_enabled') or []
            if 'lh' in channelmodulesarray:
                rando = random.randint(1,10000)
                rand = str(rando)
                osd(bot, trigger.sender, 'say', ["[Lifehack Number", rand,"]", message, "[Lifehack]"])


# compare timestamps
def time_since(bot, nick, databasekey):
    """Figure out when the last ad was."""
    now = time.time()
    last = get_database_value(bot, nick, databasekey)
    return abs(now - int(last))
