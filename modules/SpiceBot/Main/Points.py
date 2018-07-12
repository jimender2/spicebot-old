#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from random import random
from random import randint
from sopel import module, tools
import string
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
    pointsstring = trigger.group(1)
    pointsreason = get_trigger_arg(bot, triggerargsarray, '2+')
    pointsreasonmsg = '.'
    if not channel.startswith("#"):
        bot.notice(instigator + ", " + pointsstring.title() + " must be in a channel.", instigator)
        return
    rando = randint(1, 666)
    commortarget = get_trigger_arg(bot, triggerargsarray, 1)
    botusersarray = get_database_value(bot, bot.nick, 'botusers') or []

    if not commortarget:
        commortarget = 'everyone'

    if commortarget == instigator:
        bot.say("You cannot award " + pointsstring + " to yourself!")

    elif commortarget == "check":
        target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
        if target.lower() not in [u.lower() for u in bot.users]:
            bot.say("I'm not sure who that is.")
            return
        points = get_database_value(bot, target, 'points') or 0
        if not points:
            bot.say(target + ' has no ' + pointsstring + ' history.')
        else:
            bot.say(target + ' has ' + str(points) + ' ' + pointsstring + '.')

    elif commortarget == 'all' or commortarget == 'everybody' or commortarget == 'everyone':
        if pointsreason:
            if pointsreason.startswith('for'):
                pointsreasonmsg = ' ' + str(pointsreason) + '.'
            else:
                pointsreasonmsg = ' for ' + str(pointsreason) + '.'
            if pointsreason[-1] not in string.punctuation:
                pointsreason = pointsreason + "."
        randopoints = str(instigator + " awards " + str(rando) + ' ' + pointsstring + ' to everyone'+ str(pointsreasonmsg))
        bot.say(randopoints)
        for u in bot.users:
            if u in botusersarray and u != bot.nick and u != instigator:
                adjust_database_value(bot, u, 'points', rando)

    elif commortarget == 'take':
        target = get_trigger_arg(bot, triggerargsarray, 2)
        pointsreason = get_trigger_arg(bot, triggerargsarray, '3+')
        if pointsreason:
            if pointsreason.startswith('for'):
                pointsreasonmsg = ' ' + str(pointsreason) + '.'
            else:
                pointsreasonmsg = ' for ' + str(pointsreason) + '.'
            if pointsreason[-1] not in string.punctuation:
                pointsreason = pointsreason + "."
        if not target:
            target = 'everyone'
        if target == instigator:
            bot.say("You cannot take " + pointsstring + " from yourself!")
        elif target == 'all' or target == 'everybody' or target == 'everyone':
            randopoints = str(instigator + " takes " + str(rando) + ' ' + pointsstring + ' from everyone' + str(pointsreasonmsg))
            bot.say(randopoints)
            for u in bot.users:
                if u in botusersarray and u != bot.nick and u != instigator:
                    adjust_database_value(bot, u, 'points', -abs(rando))
        elif target.lower() not in [u.lower() for u in bot.users]:
            bot.say("I'm not sure who that is.")
        else:
            randopoints = str(instigator + " takes " + str(rando) + " " + pointsstring + " from " + target + str(pointsreasonmsg))
            bot.say(randopoints)
            adjust_database_value(bot, target, 'points', -abs(rando))

    elif commortarget == 'low':
        target = get_trigger_arg(bot, triggerargsarray, 2)
        pointsreason = get_trigger_arg(bot, triggerargsarray, '3+')
        rando = randint(1, 333)
        if pointsreason:
            if pointsreason.startswith('for'):
                pointsreasonmsg = ' ' + str(pointsreason) + '.'
            else:
                pointsreasonmsg = ' for ' + str(pointsreason) + '.'
            if pointsreason[-1] not in string.punctuation:
                pointsreason = pointsreason + "."
            if not target:
                target = 'everyone'
        if target == instigator:
            bot.say("You cannot give " + pointsstring + " to yourself!")
        elif target == 'all' or target == 'everybody' or target == 'everyone':
            randopoints = str(instigator + " gives " + str(rando) + ' ' + pointsstring + ' to everyone' + str(pointsreasonmsg))
            bot.say(randopoints)
            for u in bot.users:
                if u in botusersarray and u != bot.nick and u != instigator:
                    adjust_database_value(bot, u, 'points', abs(rando))
        elif target.lower() not in [u.lower() for u in bot.users]:
            bot.say("I'm not sure who that is.")
        else:
            randopoints = str(instigator + " gives " + str(rando) + " " + pointsstring + " to " + target + str(pointsreasonmsg))
            bot.say(randopoints)
            adjust_database_value(bot, target, 'points', abs(rando))

    elif commortarget == 'high':
        target = get_trigger_arg(bot, triggerargsarray, 2)
        pointsreason = get_trigger_arg(bot, triggerargsarray, '3+')
        rando = randint(334, 666)
        if pointsreason:
            if pointsreason[-1] not in string.punctuation:
                pointsreason = pointsreason + "."
            if pointsreason.startswith('for'):
                pointsreasonmsg = ' ' + str(pointsreason) + '.'
            else:
                pointsreasonmsg = ' for ' + str(pointsreason) + '.'
        if not target:
            target = 'everyone'
        if target == instigator:
            bot.say("You cannot give " + pointsstring + " to yourself!")
        elif target == 'all' or target == 'everybody' or target == 'everyone':
            randopoints = str(instigator + " gives " + str(rando) + ' ' + pointsstring + ' from everyone' + str(pointsreasonmsg))
            bot.say(randopoints)
            for u in bot.users:
                if u in botusersarray and u != bot.nick and u != instigator:
                    adjust_database_value(bot, u, 'points', abs(rando))
        elif target.lower() not in [u.lower() for u in bot.users]:
            bot.say("I'm not sure who that is.")
        else:
            randopoints = str(instigator + " gives " + str(rando) + " " + pointsstring + " to " + target + str(pointsreasonmsg))
            bot.say(randopoints)
            adjust_database_value(bot, target, 'points', abs(rando))

    elif commortarget == 'except':
        target = get_trigger_arg(bot, triggerargsarray, 2)
        pointsreason = get_trigger_arg(bot, triggerargsarray, '3+')
        if pointsreason:
            if pointsreason[-1] not in string.punctuation:
                pointsreason = pointsreason + "."
            if pointsreason.startswith('for'):
                pointsreasonmsg = ' ' + str(pointsreason) + '.'
            else:
                pointsreasonmsg = ' for ' + str(pointsreason) + '.'
        if not target:
            randopoints = "Oh sure. Who are you leaving out now?"
        elif target == 'all' or target == 'everybody' or target == 'everyone':
            randopoints = "That doesn't work, moron."
            bot.say(randopoints)
        elif target.lower() not in [u.lower() for u in bot.users]:
            bot.say("I'm not sure who that is.")
        else:
            randopoints = str(instigator + " gives " + str(rando) + " " + pointsstring + " to everyone except " + target + str(pointsreasonmsg))
            bot.say(randopoints)
            for u in bot.users:
                if u in botusersarray and u != bot.nick and u != instigator and u != target:
                    adjust_database_value(bot, u, 'points', abs(rando))

    elif commortarget.lower() not in [u.lower() for u in bot.users]:
        bot.say("I'm not sure who that is.")
    else:
        if pointsreason:
            if pointsreason[-1] not in string.punctuation:
                pointsreason = pointsreason + "."
            if pointsreason.startswith('for'):
                pointsreasonmsg = ' ' + str(pointsreason)
            else:
                pointsreasonmsg = ' for ' + str(pointsreason)
        randopoints = str(instigator + " awards " + str(rando) + ' ' + pointsstring + ' to '+commortarget+str(pointsreasonmsg))
        bot.say(randopoints)
        adjust_database_value(bot, commortarget, 'points', rando)

def addpoints(bot, target, amount):
    adjust_database_value(bot, target, 'points', abs(amount))

def takepoints(bot, target, amount):
    adjust_database_value(bot, target, 'points', -abs(amount))
