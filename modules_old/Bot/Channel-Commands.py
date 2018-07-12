#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel import module, tools
from sopel.module import ADMIN
from sopel.module import VOICE
from sopel.module import event, rule
from sopel.module import OP
from sopel.tools.target import User, Channel
import time
import os
import sys
import fnmatch
import re
import git 
from os.path import exists
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('channel')
def main_command(bot, trigger):
    instigator = trigger.nick
    triggerargsarray = get_trigger_arg(bot, trigger.group(2), 'create')
    subcommand = get_trigger_arg(bot, triggerargsarray, 1)
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray = special_users(bot)
    
    ## list channels
    if not subcommand:
        channelarray = []
        for c in bot.channels:
            channelarray.append(c)
        chanlist = get_trigger_arg(bot, channelarray, 'list')
        bot.say("You can find me in " + chanlist)
        
    ## OP list
    elif subcommand.lower() == 'op':
        oplist = get_trigger_arg(bot, operatorarray, 'list')
        bot.notice("Channel Operators are: " + oplist, instigator)
        
    ## Voice List
    elif subcommand.lower() == 'voice':
        voicelist = get_trigger_arg(bot, voicearray, 'list')
        bot.notice("Channel VOICE are: " + voicelist, instigator)
  
