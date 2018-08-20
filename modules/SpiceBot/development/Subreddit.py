#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author deathbybandaid


@sopel.module.commands('subreddit')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)


def execute_main(bot, trigger, triggerargsarray):
    osd(bot, trigger.sender, 'say', "do the thing")


# respond to alternate start for command
@module.rule('^(?:r/)\s+?.*')
@sopel.module.thread(True)
def mainfunctionnobeguine(bot, trigger):
    command_type = 'normalcom'
    triggerargsarray = get_trigger_arg(bot, trigger.group(0), 'create')
    triggerargsarray = get_trigger_arg(bot, triggerargsarray, '2+')
    triggerargsarray = get_trigger_arg(bot, triggerargsarray, 'create')
    execute_main(bot, trigger, triggerargsarray)
