#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
# sopel imports
import sopel.module
from sopel.module import commands, nickname_commands, rule, priority, example, OP, ADMIN, VOICE, event, rule
from sopel.formatting import bold
import sopel
from sopel import module, tools, formatting

from .Database_adjust import *
from .Array_manipulation import *
from .Display_Text import *
from .RPG_Class import *
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

    # No Empty Commands
    if triggerargsarray == []:
        osd_notice(bot, trigger.nick, "No Command issued.")
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
    if instigator in [u'SpiceBotdev', u'spiceRPGdev', u'dysonparkes', u'jimender2_away', u'SpiceDuelsdev', u'deathbybandaid', u'm4virus1', u'under_score', u'sideone', u'bucketm0use', u'jimender2', u'SpiceDirect', u'Tartanarmy', u'kez|library']:
        bot.say("in there")
    else:
        bot.say("not in there")

    return

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
        command_full = get_trigger_arg(bot, rpg.triggerargsarray, 0)
        command_main = get_trigger_arg(bot, rpg.triggerargsarray, 1)

        # Run command process
        # command_main_process(bot, trigger, rpg)
        onscreentext(bot, trigger.nick, command_full)
