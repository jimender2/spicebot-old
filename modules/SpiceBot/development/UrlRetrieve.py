#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import urllib
import sys
import os
from word2number import w2n
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

address = 'https://raw.githubusercontent.com/SpiceBot/SpiceBot/master/Text-Files/ferengi_rules.txt'


@sopel.module.commands('getline')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'testline')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Get a line from the given url."""
    line = get_trigger_arg(bot, triggerargsarray, 0) or 'random'
    message = retrieveurlline(bot, address, line)
    osd(bot, trigger.sender, 'say', message)


def retrieveurlline(bot, fileurl, lineno):
    """Retrieve specified line from given url."""
    if not lineno:
        myline = randomurlline()
    else:
        lineno.lstrip("-")
        if (line == '0' or lineno.lower() == 'zero'):
            myline = 'That doesnt appear to be a rule number.'
        elif requested == 'random':
            myline = randomurlline(bot, fileurl)
        else:
            htmlfile = urllib.urlopen(fileurl)
            lines = htmlfile.readlines()
            numberoflines = len(lines)

            if lineno.isdigit():
                linenumber = int(requested)
                if linenumber > numberoflines:
                    myline = "Please select a line number between 1 and " + str(numberoflines) + "."
                else:
                    myline = get_trigger_arg(bot, lines, linenumber)
            else:
                try:
                    linenumber = w2n.word_to_num(str(requested))
                    myline = get_trigger_arg(bot, lines, linenumber)
                except ValueError:
                    myline = "That number doesn't appear to have anything associated with it."
    if not myline or myline == '\n':
        myline = 'There is nothing tied to this number.'


def randomurlline(bot, address):
    """Retrieve random line from given raw file."""
    htmlfile = urllib.urlopen(address)
    lines = htmlfile.read().splitlines()
    myline = random.choice(lines)
    if not myline or myline == '\n':
        myline = randomline()
    return myline
