#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

from .Global_Vars import *

"""
On Screen Text
"""


def osd_notice(bot, target, textarraycomplete):
    target = nick_actual(bot,target)
    if not isinstance(textarraycomplete, list):
        texttoadd = str(textarraycomplete)
        textarraycomplete = []
        textarraycomplete.append(texttoadd)
    passthrough = []
    passthrough.append(target + ", ")
    for x in textarraycomplete:
        passthrough.append(x)
    onscreentext(bot, [target], passthrough)


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
        target = nick_actual(bot,str(target_array))
        texttargetarray.append(target)
    else:
        for target in target_array:
            target = nick_actual(bot,str(target_array))
            texttargetarray.append(target)

    # Make sure we don't cross over IRC limits
    combinedtextarray = []
    currentstring = ''
    for textstring in textarraycomplete:
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

    # Display the text
    for target in texttargetarray:
        if text_type == 'notice':
            combinedtextarray.insert(0, target + ", ")
        textparts = len(combinedtextarray)
        textpartsleft = textparts
        for combinedline in combinedtextarray:
            textpartsleft = textpartsleft - 1
            if text_type == 'say':
                bot.say(combinedline)
            elif target.startswith("#"):
                bot.msg(target, combinedline)
            elif text_type == 'notice':
                bot.notice(combinedline, target)
            elif text_type == 'action' and textpartsleft == textparts:
                bot.action(combinedline,user)
            else:
                bot.say(combinedline)


def onscreentext(bot, texttargetarray, textarraycomplete):
    if not isinstance(textarraycomplete, list):
        texttoadd = str(textarraycomplete)
        textarraycomplete = []
        textarraycomplete.append(texttoadd)
    if not isinstance(texttargetarray, list):
        target = texttargetarray
        texttargetarray = []
        texttargetarray.append(target)
    combinedtextarray = []
    currentstring = ''
    for textstring in textarraycomplete:
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
    for combinedline in combinedtextarray:
        for user in texttargetarray:
            if user == 'say':
                bot.say(combinedline)
            elif user.startswith("#"):
                bot.msg(user, combinedline)
            else:
                bot.notice(combinedline, user)


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
