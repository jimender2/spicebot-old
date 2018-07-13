#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
# sopel imports
import sopel.module
from sopel.module import commands, nickname_commands, rule, priority, example, OP, ADMIN, VOICE, event, rule
import sopel
from sopel import module, tools

# from .Database_adjust import *
# from .Array_manipulation import *
# from .Display_Text import *

from ...BotShared import *


# basic test
@sopel.module.commands('rpgtest')
@sopel.module.thread(True)
def rpg_test(bot, trigger):
    onscreentext(bot, trigger.nick, "I'm alive")
    # bot.say("I'm alive")
