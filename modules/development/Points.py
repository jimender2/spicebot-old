#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from random import random
from random import randint
from sopel import module, tools
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('points','pants')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'points')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    channel = trigger.sender
    instigator = trigger.nick
    if not channel.startswith("#"):
        bot.notice(instigator + " Points must be in a channel.", instigator)
        return
    rando = randint(1, 666)
    commortarget = get_trigger_arg(triggerargsarray, 1)
    botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
    if not commortarget:
        commortarget = 'everyone'
    if commortarget == instigator:
        bot.say("You cannot award points to yourself!")
    elif commortarget == "check":
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target.lower() not in [u.lower() for u in bot.users]:
            bot.say("I'm not sure who that is.")
            return
        points = get_botdatabase_value(bot, target, 'points') or 0
        if not points:
            bot.say(target + ' has no points history.')
        else:
            bot.say(target + ' has ' + str(points) + ' points.')
    elif commortarget == 'all' or commortarget == 'everybody' or commortarget == 'everyone':
        randopoints = str(instigator + " awards " + str(rando) + ' points to everyone.')
        bot.say(randopoints)
        for u in bot.users:
            if u in botusersarray and u != bot.nick and u != instigator:
                adjust_botdatabase_value(bot, u, 'points', rando)
    elif commortarget == "take":
        target = get_trigger_arg(triggerargsarray, 2)
        if not target:
            commortarget = 'everyone'
        if target == instigator:
            bot.say("You cannot take points from yourself!")
        elif target == 'all' or target == 'everybody' or target == 'everyone':
            randopoints = str(instigator + " takes " + str(rando) + ' points from everyone.')
            bot.say(randopoints)
            for u in bot.users:
                if u in botusersarray and u != bot.nick and u != instigator:
                    adjust_botdatabase_value(bot, u, 'points', -abs(rando))
        elif target.lower() not in [u.lower() for u in bot.users]:
            bot.say("I'm not sure who that is.")
        else:
            randopoints = str(instigator + " takes " + str(rando) + " points from " + target + ".")
            bot.say(randopoints)
            adjust_botdatabase_value(bot, target, 'points', -abs(rando))
    elif commortarget.lower() not in [u.lower() for u in bot.users]:
        bot.say("I'm not sure who that is.")
    else:
        randopoints = str(instigator + " awards " + str(rando) + ' points to '+commortarget+'.')
        bot.say(randopoints)
        adjust_botdatabase_value(bot, commortarget, 'points', rando)
