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
    rpg = rpg_class()
    triggerargsarray = get_trigger_arg(bot, trigger.group(2), 'create')
    execute_main(bot, trigger, triggerargsarray, rpg)


# respond to alternate start for command
@module.rule('^(?:rpg)\s+?.*')
@module.rule('^(?:!rpg)\s+?.*')
@module.rule('^(?:,rpg)\s+?.*')
@sopel.module.thread(True)
def rpg_trigger_precede(bot, trigger):
    rpg = rpg_class()
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
    rpg.instigator = trigger.nick
    bot.say(str(trigger))
    instigator = rpg_instigator()
    bot.say(str(instigator))
    instigator.name = trigger.nick
    bot.say(str(instigator.name))

    bot.say("other test")

    class rpg_instigatortest():
        pass
    instigatortest = rpg_instigatortest()
    instigatortest.chan = trigger.sender

    return

    # Cycle through command array
    for command_split_partial in rpg.multi_com_list:
        rpg.triggerargsarray = get_trigger_arg(bot, command_split_partial, 'create')

        # Admin only
        rpg.admin = 0
        if [x for x in triggerargsarray_part if x == "-a"]:
            triggerargsarray_part.remove("-a")
            if trigger.admin:
                rpg.admin = 1

        # Split commands to pass
        command_full = get_trigger_arg(bot, triggerargsarray_part, 0)
        command_main = get_trigger_arg(bot, triggerargsarray_part, 1)

        # Run command process
        command_main_process(bot, trigger, rpg)
    onscreentext(bot, trigger.nick, triggerargsarray)
