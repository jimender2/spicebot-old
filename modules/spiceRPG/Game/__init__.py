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
    if triggerargsarray == []:
        osd_notice(bot, trigger.nick, "No Command issued.")
        return
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
    if triggerargsarray == []:
        osd_notice(bot, trigger.nick, "No Command issued.")
        return
    execute_main(bot, trigger, triggerargsarray, rpg)


def execute_main(bot, trigger, triggerargsarray, rpg):
    onscreentext(bot, trigger.nick, triggerargsarray)
