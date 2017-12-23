#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
from sopel.module import OP
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('msg', 'nick', 'attach', 'server', 'join', 'whois', 'me', 'ban')
def execute_main(bot, trigger):
    trigger = trigger.replace('.', '/', 1)
    bot.say('I believe you wanted to say ' + trigger)
                
