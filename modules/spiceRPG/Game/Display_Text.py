#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

from .Global_Vars import *

"""
On Screen Text
"""


def dummytest(weapons):
    chunks = weapons.split()
    per_line = 15
    weaponline = ''
    for i in range(0, len(chunks), per_line):
        weaponline = " ".join(chunks[i:i + per_line])
        bot.notice(str(weaponline), instigator)


def osd(bot, target_array, text_type, text_array):

    # if text_array is a string, make it an array
    textarraycomplete = []
    if not isinstance(text_array, list):
        textarraycomplete.append(str(text_array))
    else:
        for x in text_array:
            textarraycomplete.append(str(x))

    # if target_array is a string, make it an array
    texttargetarray = []
    if not isinstance(target_array, list):
        if not str(target_array).startswith("#"):
            target_array = nick_actual(bot,str(target_array))
        texttargetarray.append(target_array)
    else:
        for target in target_array:
            if not str(target).startswith("#"):
                target = nick_actual(bot,str(target))
            texttargetarray.append(target)

    # Make sure we don't cross over IRC limits
    for target in texttargetarray:
        temptextarray = []
        if text_type == 'notice':
            temptextarray.append(target + ", ")
        for part in textarraycomplete:
            temptextarray.append(part)

        combinedtextarray = []
        currentstring = ''
        combinationcount = 0
        for textstring in temptextarray:
            bot.say(str(combinationcount))
            if currentstring == '':
                currentstring = textstring
            elif len(textstring) > osd_limit:
                if currentstring != '':
                    combinedtextarray.append(currentstring)
                    currentstring = ''
                combinedtextarray.append(textstring)
            else:
                tempstring = str(currentstring + "   " + textstring)
                if len(tempstring) <= osd_limit:
                    currentstring = tempstring
                else:
                    combinedtextarray.append(currentstring)
                    currentstring = textstring
            combinationcount = combinationcount + 1
        if currentstring != '':
            combinedtextarray.append(currentstring)

        # display
        textparts = len(combinedtextarray)
        textpartsleft = textparts
        for combinedline in combinedtextarray:
            if text_type == 'say':
                bot.say(combinedline)
            elif text_type == 'action' and textparts == textpartsleft:
                bot.action(combinedline,target)
            elif str(target).startswith("#"):
                bot.msg(target, combinedline)
            elif text_type == 'notice':
                bot.notice(combinedline, target)
            else:
                bot.say(combinedline)
            textpartsleft = textpartsleft - 1


"""
How to Display Nicks
"""


# Outputs Nicks with correct capitalization
def nick_actual(bot,nick):
    actualnick = nick
    for u in bot.users:
        if u.lower() == actualnick.lower():
            actualnick = u
            continue
    return actualnick
