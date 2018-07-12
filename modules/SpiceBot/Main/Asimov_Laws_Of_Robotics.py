#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
from word2number import w2n
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

@sopel.module.commands('asimov')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    requested = get_trigger_arg(bot,triggerargsarray, 0)
    laws = ['may not injure a human being or, through inaction, allow a human being to come to harm.', 'must obey orders given it by human beings except where such orders would conflict with the First Law.', 'must obey orders given it by human beings except where such orders would conflict with the First Law.', 'must protect its own existence as long as such protection does not conflict with the First or Second Law.', 'must comply with all chatroom rules.']
    if not requested:
        myline = get_trigger_arg(bot, laws, 'random')
    else:
        requested.lstrip("-")
        if (requested == '0' or requested.lower()) == 'zero':
            myline=''
        else:
            if requested.isdigit():
                myline = get_trigger_arg(bot, laws, requested)
            else:
                try:
                    requested = w2n.word_to_num(str(requested))
                    myline = get_trigger_arg(bot, laws, requested)
                except ValueError:
                    myline=''

    #bot.action('may not injure a human being or, through inaction, allow a human being to come to harm.')
    #bot.action('must obey orders given it by human beings except where such orders would conflict with the First Law.')
    #bot.action('must protect its own existence as long as such protection does not conflict with the First or Second Law.')
    #bot.action('must comply with all chatroom rules.')
    if not myline:
        myline=myline = get_trigger_arg(bot, laws, 'random')
    bot.action(str(myline))
