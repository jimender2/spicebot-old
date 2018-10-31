#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
from sopel.module import OP
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('ircmistakes', 'msg', 'nick', 'attach', 'server', 'join', 'whois', 'me', 'ban', 'kick')
def execute_main(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'ircmistakes')
    if trigger.group(1) == "whois" and trigger.group(2).lower() == "therealslimshady":
        osd(bot, trigger.sender, 'say', "Im Slim Shady, yes I'm the real Shady.")
        osd(bot, trigger.sender, 'action', "stands up.")
    else:
        osd(bot, trigger.sender, 'say', 'I believe you wanted to say ' + "/" + trigger.group(1) + " " + spicemanip(bot, triggerargsarray, 0))
