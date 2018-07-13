#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
# sopel imports
import sopel.module
from sopel.module import commands, nickname_commands, rule, priority, example, OP, ADMIN, VOICE, event, rule
from sopel.formatting import bold
import sopel
from sopel import module, tools, formatting


# basic test
@sopel.module.commands('rpgtest')
@sopel.module.thread(True)
def color_test(bot, trigger):
    bot.say(formatting.color('Purple', formatting.colors.PURPLE))
    bot.say(bold('bold'))
