#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

from .Global_Vars import *

"""
On Screen Text
"""


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
        if not target.startswith("#"):
            target = nick_actual(bot,str(target_array))
        texttargetarray.append(target)
    else:
        for target in target_array:
            if not target.startswith("#"):
                target = nick_actual(bot,str(target_array))
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
        for textstring in temptextarray:
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
        if currentstring != '':
            combinedtextarray.append(currentstring)

        # display
        textparts = len(combinedtextarray)
        textpartsleft = textparts
        for combinedline in combinedtextarray:
            # bot.say(str(textpartsleft) + " " + str(textparts))
            if text_type == 'say':
                bot.say(combinedline)
            elif text_type == 'action' and textparts == textpartsleft:
                bot.action(combinedline,target)
            elif target.startswith("#"):
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
