#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module


# imports for system and OS access, directories
import os
import sys

# imports based on THIS file
from BotShared import *
from random import random
import string
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

comdict = {
            "author": "deathbybandaid",
            "contributors": [],
            "description": "A module to give and take points from channel denizens.",
            'privs': [],
            "example": ".points dysonparkes",
            "exampleresponse": "$instigator gives $randomnumber points to $target for $reason",
            }


@sopel.module.commands('points', 'pants')
def mainfunction(bot, trigger):
    """Create argument lists and confirm module is active."""
    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    if not botcom.multiruns:
        execute_main(bot, trigger, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip.main(botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip.main(command_split_partial, 'create')
            execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):
    """Do the thing."""
    channel = trigger.sender
    instigator = trigger.nick
    pointsstring = trigger.group(1)
    pointsreason = spicemanip.main(botcom.triggerargsarray, '2+')
    pointsreasonmsg = '.'
    if not channel.startswith("#"):
        osd(bot, trigger.nick, 'notice', pointsstring.title() + " must be in a channel.")
        return
    rando = randint(1, 666)
    commortarget = spicemanip.main(botcom.triggerargsarray, 1)
    botusersarray = get_database_value(bot, bot.nick, 'botusers') or []

    if not commortarget:
        commortarget = 'everyone'

    if commortarget == instigator:
        osd(bot, trigger.sender, 'say', "You cannot award " + pointsstring + " to yourself!")

    elif commortarget == "check":
        target = spicemanip.main(botcom.triggerargsarray, 2) or instigator
        if target.lower() not in [u.lower() for u in bot.users]:
            osd(bot, trigger.sender, 'say', "I'm not sure who that is.")
            return
        points = get_database_value(bot, target, 'points') or 0
        if not points:
            osd(bot, trigger.sender, 'say', target + ' has no ' + pointsstring + ' history.')
        else:
            osd(bot, trigger.sender, 'say', target + ' has ' + str(points) + ' ' + pointsstring + '.')

    elif commortarget == 'all' or commortarget == 'everybody' or commortarget == 'everyone':
        if pointsreason:
            if pointsreason.startswith('for'):
                pointsreasonmsg = ' ' + str(pointsreason) + '.'
            else:
                pointsreasonmsg = ' for ' + str(pointsreason) + '.'
            if pointsreason[-1] not in string.punctuation:
                pointsreason = pointsreason + "."
        randopoints = str(instigator + " awards " + str(rando) + ' ' + pointsstring + ' to everyone' + str(pointsreasonmsg))
        osd(bot, trigger.sender, 'say', randopoints)
        for u in bot.users:
            if u in botusersarray and u != bot.nick and u != instigator:
                adjust_database_value(bot, u, 'points', rando)

    elif commortarget == 'take':
        target = spicemanip.main(botcom.triggerargsarray, 2)
        pointsreason = spicemanip.main(botcom.triggerargsarray, '3+')
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
            if pointsstring == 'pants':
                osd(bot, trigger.sender, 'say', "No " + instigator + ", I will not help you take your " + pointsstring + " off!")
            else:
                osd(bot, trigger.sender, 'say', "You cannot take " + pointsstring + " from yourself!")
        elif target == 'all' or target == 'everybody' or target == 'everyone':
            randopoints = str(instigator + " takes " + str(rando) + ' ' + pointsstring + ' from everyone' + str(pointsreasonmsg))
            osd(bot, trigger.sender, 'say', randopoints)
            for u in bot.users:
                if u in botusersarray and u != bot.nick and u != instigator:
                    adjust_database_value(bot, u, 'points', -abs(rando))
        elif target.lower() not in [u.lower() for u in bot.users]:
            osd(bot, trigger.sender, 'say', "I'm not sure who that is.")
        else:
            randopoints = str(instigator + " takes " + str(rando) + " " + pointsstring + " from " + target + str(pointsreasonmsg))
            osd(bot, trigger.sender, 'say', randopoints)
            adjust_database_value(bot, target, 'points', -abs(rando))

    elif commortarget == 'low':
        target = spicemanip.main(botcom.triggerargsarray, 2)
        pointsreason = spicemanip.main(botcom.triggerargsarray, '3+')
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
            osd(bot, trigger.sender, 'say', "You cannot give " + pointsstring + " to yourself!")
        elif target == 'all' or target == 'everybody' or target == 'everyone':
            randopoints = str(instigator + " gives " + str(rando) + ' ' + pointsstring + ' to everyone' + str(pointsreasonmsg))
            osd(bot, trigger.sender, 'say', randopoints)
            for u in bot.users:
                if u in botusersarray and u != bot.nick and u != instigator:
                    adjust_database_value(bot, u, 'points', abs(rando))
        elif target.lower() not in [u.lower() for u in bot.users]:
            osd(bot, trigger.sender, 'say', "I'm not sure who that is.")
        else:
            randopoints = str(instigator + " gives " + str(rando) + " " + pointsstring + " to " + target + str(pointsreasonmsg))
            osd(bot, trigger.sender, 'say', randopoints)
            adjust_database_value(bot, target, 'points', abs(rando))

    elif commortarget == 'high':
        target = spicemanip.main(botcom.triggerargsarray, 2)
        pointsreason = spicemanip.main(botcom.triggerargsarray, '3+')
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
            osd(bot, trigger.sender, 'say', "You cannot give " + pointsstring + " to yourself!")
        elif target == 'all' or target == 'everybody' or target == 'everyone':
            randopoints = str(instigator + " gives " + str(rando) + ' ' + pointsstring + ' from everyone' + str(pointsreasonmsg))
            osd(bot, trigger.sender, 'say', randopoints)
            for u in bot.users:
                if u in botusersarray and u != bot.nick and u != instigator:
                    adjust_database_value(bot, u, 'points', abs(rando))
        elif target.lower() not in [u.lower() for u in bot.users]:
            osd(bot, trigger.sender, 'say', "I'm not sure who that is.")
        else:
            randopoints = str(instigator + " gives " + str(rando) + " " + pointsstring + " to " + target + str(pointsreasonmsg))
            osd(bot, trigger.sender, 'say', randopoints)
            adjust_database_value(bot, target, 'points', abs(rando))

    elif commortarget == 'except':
        target = spicemanip.main(botcom.triggerargsarray, 2)
        pointsreason = spicemanip.main(botcom.triggerargsarray, '3+')
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
            osd(bot, trigger.sender, 'say', randopoints)
        elif target.lower() not in [u.lower() for u in bot.users]:
            osd(bot, trigger.sender, 'say', "I'm not sure who that is.")
        else:
            randopoints = str(instigator + " gives " + str(rando) + " " + pointsstring + " to everyone except " + target + str(pointsreasonmsg))
            osd(bot, trigger.sender, 'say', randopoints)
            for u in bot.users:
                if u in botusersarray and u != bot.nick and u != instigator and u != target:
                    adjust_database_value(bot, u, 'points', abs(rando))

    elif commortarget.lower() not in [u.lower() for u in bot.users]:
        osd(bot, trigger.sender, 'say', "I'm not sure who that is.")
    else:
        if pointsreason:
            if pointsreason[-1] not in string.punctuation:
                pointsreason = pointsreason + "."
            if pointsreason.startswith('for'):
                pointsreasonmsg = ' ' + str(pointsreason)
            else:
                pointsreasonmsg = ' for ' + str(pointsreason)
        randopoints = str(instigator + " awards " + str(rando) + ' ' + pointsstring + ' to '+commortarget+str(pointsreasonmsg))
        osd(bot, trigger.sender, 'say', randopoints)
        adjust_database_value(bot, commortarget, 'points', rando)


def addpoints(bot, target, amount):
    """Increase points of a target."""
    adjust_database_value(bot, target, 'points', abs(amount))


def takepoints(bot, target, amount):
    """Decrease points of a target."""
    adjust_database_value(bot, target, 'points', -abs(amount))
