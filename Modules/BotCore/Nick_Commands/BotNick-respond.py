#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module

# imports for system and OS access, directories
import os
import sys

# imports based on THIS file
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


"""
This will respond to all other invalid coms
"""


@nickname_commands('(.*)')
@sopel.module.thread(True)
def bot_nickcom_hub(bot, trigger):

    botcom = botcom_nick(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    if not botcom.command_main:
        return osd(bot, botcom.channel_current, 'say', "I don't know what you are asking me to do!")
    if str(bot.nick) + " " + botcom.command_main.lower() in bot.memory["botdict"]["tempvals"]["nickname_commands"].keys():
        return

    specialcomposs = spicemanip(bot, botcom.triggerargsarray, 0).lower()
    if specialcomposs.lower().startswith("what is"):
        searchterm = spicemanip(bot, botcom.triggerargsarray, "3+") or None
        if searchterm:
            osd(bot, botcom.channel_current, 'say', "What is " + searchterm)
            osd(bot, botcom.channel_current, 'say', "Do you think this is Jeopardy?")
            return
    elif specialcomposs.lower().startswith(tuple(["make me a", "beam me a"])):
        makemea = spicemanip(bot, botcom.triggerargsarray, "4+") or None
        if makemea:
            osd(bot, botcom.channel_current, 'action', " beams " + botcom.instigator + " a " + makemea)
        return
    elif specialcomposs.lower().startswith("can you see"):
        target = spicemanip(bot, botcom.triggerargsarray, "4+") or None
        if not target:
            target = 'me'
        if target in [botcom.instigator, 'me']:
            osd(bot, botcom.channel_current, 'say', botcom.instigator + ", I can see you.")
        else:
            if bot_check_inlist(bot, target, bot.memory["botdict"]["tempvals"]["servers_list"][botcom.server]['all_current_users']):
                osd(bot, botcom.channel_current, 'say', botcom.instigator + ", yes. I can see " + nick_actual(bot, target) + " right now!")
            else:
                if bot_check_inlist(bot, target, bot.memory["botdict"]["users"].keys()):
                    osd(bot, botcom.channel_current, 'say', botcom.instigator + ", I can't see " + nick_actual(bot, target) + " at the moment.")
                else:
                    osd(bot, botcom.channel_current, 'say', "I have never seen " + str(target) + ".")
        return

    if str(bot.nick) + " " + botcom.command_main.lower() not in bot.memory["botdict"]["tempvals"]["nickname_commands"].keys():
        sim_com, sim_num = [], []
        for comm in bot.memory["botdict"]["tempvals"]["nickname_commands"].keys():
            similarlevel = similar(str(bot.nick) + " " + str(botcom.command_main).lower(), comm.lower())
            if similarlevel >= .75:
                sim_com.append(comm)
                sim_num.append(similarlevel)
        if sim_com != [] and sim_num != []:
            sim_num, sim_com = array_arrangesort(bot, sim_num, sim_com)
            closestmatch = spicemanip(bot, sim_com, 'reverse', "list")
            listnumb, relist = 1, []
            for item in closestmatch:
                if listnumb <= 3:
                    relist.append(str(item))
                listnumb += 1
            closestmatches = spicemanip(bot, relist, "andlist")
            return osd(bot, botcom.channel_current, 'say', "I don't know what you are asking me to do! Did you mean: " + str(closestmatches) + "?")
        else:
            return osd(bot, botcom.channel_current, 'say', "I don't know what you are asking me to do!")
