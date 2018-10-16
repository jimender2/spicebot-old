#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib2
import json
from BeautifulSoup import BeautifulSoup
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *
gifshareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(gifshareddir)
from GifShared import *

# author jimender2


@sopel.module.commands('borg')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'borg')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    gif = getGif_all(bot, {"query": "Jeri Ryan", "searchnum": 'random'}, "Jeri Ryan", 'random')
    rand = random.randint(1,5)
    if rand == 1:
        osd(bot, trigger.sender, 'say', "Resistance is futile")
    else:
        if gif["querysuccess"]:
            osd(bot, trigger.sender, 'say', "%s Result (#%s): %s" % (gif['gifapi'].title(), gif['returnnum'], gif['returnurl']))
        else:
            osd(bot, trigger.sender, 'action', 'is not a contender for the Darwin award, thank fuck.')
