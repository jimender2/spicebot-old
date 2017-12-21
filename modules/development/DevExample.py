#!/usr/bin/env python
# coding=utf-8
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('devexample')
def mainfunction(bot, trigger):
    execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    bot.say("This is to help the dev team understand values.")
    bot.say("Trigger.nick: " + trigger.nick)
    chan = ''
    for c in bot.channels:
        chan = chan + c + ', '
    chan = chan[:-2]
    bot.say("Bot.Channels: [" + chan + ']')
    bot.say("Trigger.admin: " + str(trigger.admin))
    args = ''
    for arg in trigger.args:
        args = args + arg + ', '
    args = args[:-2]
    bot.say("Trigger.args: [" + args + "]")
    users = ''
    for u in bot.users:
        users = users + u + ', '
    users = users[:-2]
    bot.say("Bot.users: [" + users + "]")
