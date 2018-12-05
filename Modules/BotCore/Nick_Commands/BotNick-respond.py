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

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "monologue"]):
        pass

    botcom = botcom_nick(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    if not botcom.command_main:
        return osd(bot, botcom.channel_current, 'say', "I don't know what you are asking me to do!")

    if spicemanip(bot, botcom.triggerargsarray, 0).lower().startswith("what is"):
        searchterm = spicemanip(bot, botcom.triggerargsarray, "3+") or None
        if searchterm:
            osd(bot, botcom.channel_current, 'say', "What is " + searchterm)
            osd(bot, botcom.channel_current, 'say', "Do you think this is Jeopardy?")
            return
    elif spicemanip(bot, botcom.triggerargsarray, 0).lower().startswith("make me a"):
        makemea = spicemanip(bot, botcom.triggerargsarray, "4+") or None
        if makemea:
            osd(bot, botcom.channel_current, 'action', " beams " + botcom.instigator + " a " + makemea)
        return

    if botcom.command_main.lower() not in valid_botnick_commands.keys():
        sim_com, sim_num = [], []
        for comm in valid_botnick_commands.keys():
            similarlevel = similar(str(botcom.command_main).lower(), comm.lower())
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
