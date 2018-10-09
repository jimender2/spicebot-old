#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import arrow
import sys
import os
import datetime
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *
# import Spicebucks

# Commands that work in privmsg
privcmdlist = ['check', 'admin', 'bladder', 'fridge', 'admin']
# Admin Commands
admincommands = ['reset']

# Protected users
protectednicks = ['rycuda', 'Tech_Angel']
# Creator user
creatornicks = ["IT_Sean"]

drinks_list = {
                "Gatorade": {
                                "Cost": 5,
                                "RefillValue": 4,
                                "MaximumHeld": 5},
                "Water": {
                                "Cost": 2,
                                "RefillValue": 2,
                                "MaximumHeld": 10},
                "Soda": {
                                "Cost": 4,
                                "RefillValue": 3,
                                "MaximumHeld": 10},
                "Beer": {
                                "Cost": 10,
                                "RefillValue": 5,
                                "MaximumHeld": 12}
}

# Days before reclaim available
maxtime = 7

# Spicebuck reward values
firstclaim = 10
renewclaim = 5
stolenclaim = 20
masterclaim = -10  # Take, not give

player_info = {
                "fridge_items": {
                        "Gatorade": 0,
                        "Water": 0,
                        "Soda": 0,
                        "Beer": 0},
                "bladder_level": 10,
                "bladdermax": 10,
                "claimcost": 2,
                "master": "",
                "slaves": [],
                "claimedon": ""
            }


def spicebucks(bot, target, plusminus, amount):
    """Add or remove Spicebucks from account."""
    success = 'false'
    if type(amount) == int:
        inbank = bank(bot, target)
    if plusminus == 'plus':
        adjust_database_value(bot, target, 'spicebucks_bank', amount)
        success = 'true'
    elif plusminus == 'minus':
        if inbank - amount < 0:
            # osd(bot, trigger.sender, 'say', "I'm sorry, you do not have enough spicebucks in the bank to complete this transaction.")
            success = 'false'
        else:
            adjust_database_value(bot, target, 'spicebucks_bank', -amount)
            success = 'true'
    else:
        # osd(bot, trigger.sender, 'say', "The amount you entered does not appear to be a number.  Transaction failed.")
        success = 'false'
    return success  # returns simple true or false so modules can check the if tranaction was a success


def fridge_interactions(bot, target, action, item):
    """Check what's in the fridge/adjust items in fridge."""
    fridgecontents = player_info[fridge_items]
    return fridgecontents


def bladder_interactions(bot, target, action):
    """Check bladder level/increase or decrease level."""
    bladder_level = player_info[bladder_level]
    bladder_cost = player_info[claimcost]
    if bladder_level > bladder_cost:
        return true
    else:
        return false


@sopel.module.interval(1800)  # 30 minute automation
def halfhourtimer(bot):
    """Function for bladder refill on half-hour timer."""
    for u in bot.users:
        bladdercontents = bot.db.get_nick_value(u, 'bladdercapacity') or 'unused'
        if bladdercontents == 'unused':
            bladdercontents = 10
            bot.db.set_nick_value(u, 'bladdercapacity', bladdercontents)
        elif bladdercontents < bladdersize:
            bladdercontents = bladdercontents + 1
            bot.db.set_nick_value(u, 'bladdercapacity', bladdercontents)
