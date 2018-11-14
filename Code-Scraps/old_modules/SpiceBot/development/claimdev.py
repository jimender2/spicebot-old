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

privcmdlist = ['check', 'admin', 'bladder', 'fridge', 'admin']  # Commands that work in privmsg
admincommands = ['reset']  # Admin Commands
protectednicks = ['rycuda', 'Tech_Angel']  # Users who cannot be claimed
creatornicks = ["IT_Sean"]  # Users who get godlike recognition
reclaimtime = 7  # Time before a user can be claimed again

reward_info = {
                        "firstclaim": {
                                        "Value": 10,
                                        "Action": "plus"},
                        "renewclaim": {
                                        "Value": 5,
                                        "Action": "plus"},
                        "stolenclaim": {
                                        "Value": 20,
                                        "Action": "plus"},
                        "masterclaim": {
                                        "Value": 10,
                                        "Action": "minus"}
}

item_info = {
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


@sopel.module.commands('ownit')
def mainfunction(bot, trigger):
    """Check if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        # # IF "&&" is in the full input, it is treated as multiple commands, and is split
        # commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        # if commands_array == []:
        #     commands_array = [[]]
        # for command_split_partial in commands_array:
        #     triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Establish whether we're trying to claim or work with an item."""
    inchannel = trigger.sender  # Channel name
    todaydate = datetime.date.today()  # Todays date for maths
    storedate = str(todaydate)  # Todays date for storage
    botnicks = bot_config_names(bot)  # List all Bots (can't claim them either)
    instigator = trigger.nick  # who started it?

    target = spicemanip(bot, triggerargsarray, 1)  # target or action
    admintarget = spicemanip(bot, triggerargsarray, 2)  # if action, now target

    # LOAD TARGET INFO TO MEMORY (or create new)
    # LOAD INSTIGATOR INFO TO MEMORY (or create new)
    mastername = player_info[claimedby] or ''  # Who has the claim now?
    # Good to claim?
    okaytoclaim = 1

    # Make sure claims happen in channel, not privmsg
    if not inchannel.startswith("#") and target not in privcmdlist:
        okaytoclaim = 0
        osd(bot, trigger.sender, 'say', "Claims must be done in channel")

    # Handle if no target is specified
    elif not target:
        okaytoclaim = 0
        osd(bot, trigger.sender, 'say', "Who do you want to claim?")


def channel_check(bot, channel):
    """Check to see if this is a channel or a privmsg."""
    if channel in channel_list:
        return False
    else:
        return True


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
