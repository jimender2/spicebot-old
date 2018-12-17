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

comdict = {
            "author": "deathbybandaid",
            "contributors": ["dysonparkes", "Mace_Whatdo"],
            "description": "",
            'privs': [],
            "example": "",
            "exampleresponse": "",
            }

claim_gamedict = {
            "fullbladderseconds": 144400,
            "newbladderseconds": 12000,
            }


@sopel.module.commands('claim')
def mainfunctionnobeguine(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    botcom.multiruns = False

    if not botcom.multiruns:
        execute_main(bot, trigger, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    posstarget = spicemanip(bot, botcom.triggerargsarray, 1)
    if not posstarget:
        return osd(bot, botcom.channel_current, 'say', "Who do you want to claim?")
    botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, "2+", 'list')

    if botcom.channel_priv:
        return osd(bot, botcom.channel_current, 'notice', "Claims must be done in channel")

    bladder = get_nick_bladder(bot, botcom, botcom.instigator)

    if posstarget == 'bladder':
        posstarget = spicemanip(bot, botcom.triggerargsarray, 1) or 'self'
        if bot_check_inlist(bot, botcom.instigator, ['self', botcom.instigator]):
            return osd(bot, botcom.channel_current, 'say', ["Your bladder is currently at " + str(bladder.percent) + " capacity.", "Your character peed " + bladder.lastpeedisp])

        targetchecking = bot_target_check(bot, botcom, posstarget, [])
        if not targetchecking["targetgood"]:
            return osd(bot, botcom.instigator, 'say', targetchecking["error"])

        posstarget = nick_actual(bot, posstarget)
        if not bot_check_inlist(bot, posstarget, [botcom.instigator]) and not botcom.admin:
            return osd(bot, botcom.instigator, 'say', "You cannot tell how full/empty " + posstarget + "s bladder is!")

        targetbladder = get_nick_bladder(bot, botcom, posstarget)
        return osd(bot, botcom.channel_current, 'say', [posstarget + "s bladder is currently at " + str(targetbladder.percent) + " capacity.", posstarget + "s character peed " + targetbladder.lastpeedisp])

    if posstarget == 'check':
        posstarget = spicemanip(bot, botcom.triggerargsarray, 1) or 'self'
        messagelist = []
        if bot_check_inlist(bot, botcom.instigator, ['self', botcom.instigator]):
            claimdict = get_nick_claims(bot, botcom, botcom.instigator)
            if claimdict["ownedby"]:
                messagelist.append("You are currently owned by " + claimdict["ownedby"])
            if claimdict["ownings"] != []:
                messagelist.append("You currently own " + spicemanip(bot, claimdict["ownings"], "andlist"))
            if messagelist == []:
                messagelist.append("It looks like you are niether owned, nor own any others!")
            return osd(bot, botcom.instigator, 'say', messagelist)

        targetchecking = bot_target_check(bot, botcom, posstarget, [])
        if not targetchecking["targetgood"]:
            messagelist.append(targetchecking["error"])
            return osd(bot, botcom.instigator, 'say', messagelist)

        posstarget = nick_actual(bot, posstarget)

        claimdict = get_nick_claims(bot, botcom, posstarget)
        if claimdict["ownedby"]:
            messagelist.append(posstarget + " is currently owned by " + claimdict["ownedby"])
        if claimdict["ownings"] != []:
            messagelist.append(posstarget + " currently owns " + spicemanip(bot, claimdict["ownings"], "andlist"))
        if messagelist == []:
            messagelist.append("It looks like " + posstarget + " is neither owned, nor owns any others!")
        return osd(bot, botcom.channel_current, 'say', messagelist)


def set_nick_claims(bot, botcom, nickclaimer, bladder, nickclaimee):

    # set claimer ownership on claimee
    claimeedict = get_nick_claims(bot, botcom, nickclaimee)
    claimeedict["ownedby"] = nickclaimer

    # calculate duration of claim
    futuretime = time.time() + 240
    claimeedict["ownedbytime"] = futuretime

    set_nick_value(bot, nickclaimee, "long", 'claims', "claimdict", claimeedict)

    # set claimer ownership
    claimerdict = get_nick_claims(bot, botcom, nickclaimer)
    if nickclaimee not in claimerdict["ownings"]:
        claimerdict["ownings"].append(nickclaimee)
    set_nick_value(bot, nickclaimer, "long", 'claims', "claimdict", claimerdict)

    # empty bladder
    set_nick_value(bot, nickclaimer, "long", 'claims', "bladder", time.time())


def get_nick_claims(bot, botcom, nick):

    claimdict = get_nick_value(bot, nick, "long", 'claims', "claimdict") or None
    if not claimdict or not isinstance(claimdict, dict):
        claimdict = dict()
        set_nick_value(bot, nick, "long", 'claims', "claimdict", claimdict)

    if "ownedby" not in claimdict.keys():
        claimdict["ownedby"] = None

    if "ownedbytime" not in claimdict.keys():
        claimdict["ownedbytime"] = None

    if not claimdict["ownedbytime"] and claimdict["ownedby"]:
        claimdict["ownedby"] = None

    # expired claims
    if time.time() - claimdict["ownedbytime"] <= 0:
        remove_nick_claims(bot, botcom, claimdict["ownedby"], nick)
        claimdict["ownedby"] = None
        claimdict["ownedbytime"] = None

    if "ownings" not in claimdict.keys():
        claimdict["ownings"] = []
    if not not isinstance(claimdict["ownings"], list):
        claimdict["ownings"] = []
    for claimnick in claimdict["ownings"]:
        tempcheckdict = get_nick_value(bot, claimnick, "long", 'claims', "claimdict") or None
        if not tempcheckdict or not isinstance(tempcheckdict, dict):
            tempcheckdict = dict()
            set_nick_value(bot, claimnick, "long", 'claims', "claimdict", tempcheckdict)
        if "ownedbytime" not in tempcheckdict.keys():
            tempcheckdict["ownedbytime"] = None
        if not tempcheckdict["ownedbytime"] and tempcheckdict["ownedby"]:
            tempcheckdict["ownedby"] = None
        if time.time() - tempcheckdict["ownedbytime"] <= 0:
            if claimnick in claimdict["ownings"]:
                claimdict["ownings"].remove(claimnick)
            remove_nick_claims(bot, botcom, tempcheckdict["ownedby"], nick)
            tempcheckdict["ownedby"] = None
            tempcheckdict["ownedbytime"] = None
        set_nick_value(bot, claimnick, "long", 'claims', "claimdict", tempcheckdict)

    set_nick_value(bot, nick, "long", 'claims', "claimdict", claimdict)

    return claimdict


def remove_nick_claims(bot, botcom, nick, removenick):

    claimdict = get_nick_value(bot, nick, "long", 'claims', "claimdict") or None
    if not claimdict or not isinstance(claimdict, dict):
        claimdict = dict()
        set_nick_value(bot, nick, "long", 'claims', "claimdict", claimdict)

    if "ownings" not in claimdict.keys():
        claimdict["ownings"] = []
    if not not isinstance(claimdict["ownings"], list):
        claimdict["ownings"] = []

    if removenick in claimdict["ownings"]:
        claimdict["ownings"].remove(removenick)

    set_nick_value(bot, nick, "long", 'claims', "claimdict", claimdict)

    return claimdict


def get_nick_bladder(bot, botcom, nick):

    bladder = class_create('bladder')

    # get the last timestamp of bladder usage
    bladderleveltimestamp = get_nick_value(bot, nick, "long", 'claims', "bladder") or 0
    if not bladderleveltimestamp:
        bladderleveltimestamp = time.time() - claim_gamedict["newbladderseconds"]
        set_nick_value(bot, nick, "long", 'claims', "bladder", bladderleveltimestamp)

    # how long since last bladder expel, whether voluntary or not, bladder cannot be overful
    timesincebladder = time.time() - bladderleveltimestamp
    while timesincebladder > claim_gamedict["fullbladderseconds"]:
        timesincebladder = timesincebladder - claim_gamedict["fullbladderseconds"]
    set_nick_value(bot, nick, "long", 'claims', "bladder", time.time() - timesincebladder)

    bladder.lastpee = get_nick_value(bot, nick, "long", 'claims', "bladder")
    bladder.timesince = time.time() - bladder.lastpee
    bladder.percent = "{0:.0%}".format(bladder.timesince / claim_gamedict["fullbladderseconds"])
    bladder.lastpeedisp = str(str(humanized_time(bladder.timesince) + " ago"))

    return bladder
