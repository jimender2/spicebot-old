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
gifshareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(gifshareddir)
from BotShared import *
from GifShared import *


@sopel.module.commands('tenor')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, 0)
    if target != "roulette":
        query = target.replace(' ', '%20')
        query = str(query)

        i = 0
        while i < 3:
            randno = randint(0, giphylimit)
            gif, randno = getGif_tenor(query, randno)
            if gif:
                osd(bot, trigger.sender, 'say',  "Tenor Result (" + str(target) + " #" + str(randno) + "): " + gif)
                i = 5
            else:
                i = i + 1
        if i == 3:
            osd(bot, trigger.sender, 'say', "Hmm...Couldn't find a gif for that!")
    elif target == "roulette":
        gif = roulette()
        if gif:
            osd(bot, trigger.sender, 'say', "Click at your own risk! " + gif)
    else:
        osd(bot, trigger.sender, 'say', "Tell me what you're looking for!")
