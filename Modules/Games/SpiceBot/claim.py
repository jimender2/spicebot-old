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

# min and max are pre-varience
claim_gamedict = {
            "fullbladderseconds": 14400,
            "newbladderseconds": 10000,
            "durationmin": 432000,
            "durationmax": 777600,
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

    bladder = get_nick_bladder(bot, botcom.instigator)

    if posstarget == 'bladder':
        posstarget = spicemanip(bot, botcom.triggerargsarray, 1) or 'self'
        if bot_check_inlist(bot, posstarget, ['self', botcom.instigator]):
            return osd(bot, botcom.channel_current, 'say', ["Your bladder is currently at " + str(bladder.percent) + " capacity.", "Your character peed " + bladder.lastpeedisp])

        targetchecking = bot_target_check(bot, botcom, posstarget, [])
        if not targetchecking["targetgood"]:
            return osd(bot, botcom.channel_current, 'say', targetchecking["error"])

        posstarget = nick_actual(bot, posstarget)
        if not bot_check_inlist(bot, posstarget, [botcom.instigator]) and not botcom.admin:
            return osd(bot, botcom.channel_current, 'say', "You cannot tell how full/empty " + targetposession(bot, posstarget) + " bladder is!")

        targetbladder = get_nick_bladder(bot, posstarget)
        return osd(bot, botcom.channel_current, 'say', [targetposession(bot, posstarget) + " bladder is currently at " + str(targetbladder.percent) + " capacity.", targetposession(bot, posstarget) + " character peed " + targetbladder.lastpeedisp])

    elif posstarget == 'check':
        posstarget = spicemanip(bot, botcom.triggerargsarray, 1) or 'self'
        messagelist = []
        if bot_check_inlist(bot, posstarget, ['self', botcom.instigator]):
            claimdict = get_nick_claims(bot, botcom.instigator)
            if claimdict["ownedby"]:
                messagelist.append("You are currently owned by " + claimdict["ownedby"])
            if claimdict["ownings"] != []:
                messagelist.append("You currently own " + spicemanip(bot, claimdict["ownings"], "andlist"))
            if messagelist == []:
                messagelist.append("It looks like you are niether owned, nor own any others!")
            return osd(bot, botcom.channel_current, 'say', messagelist)

        targetchecking = bot_target_check(bot, botcom, posstarget, [])
        if not targetchecking["targetgood"]:
            return osd(bot, botcom.channel_current, 'say', targetchecking["error"])

        posstarget = nick_actual(bot, posstarget)

        claimdict = get_nick_claims(bot, posstarget)
        if claimdict["ownedby"]:
            messagelist.append(posstarget + " is currently owned by " + claimdict["ownedby"])
        if claimdict["ownings"] != []:
            messagelist.append(posstarget + " currently owns " + spicemanip(bot, claimdict["ownings"], "andlist"))
        if messagelist == []:
            messagelist.append("It looks like " + posstarget + " is neither owned, nor owns any others!")
        return osd(bot, botcom.channel_current, 'say', messagelist)

    # actual claiming
    else:
        target = posstarget

        claimerdict = get_nick_claims(bot, botcom.instigator)

        if bot_check_inlist(bot, target, [botcom.instigator]):
            osd(bot, botcom.channel_current, 'say', "You can't claim yourself!")
            osd(bot, botcom.channel_current, 'action', 'mutters "moron".')
            return

        if bot_check_inlist(bot, target, [str(bot.nick)]):
            osd(bot, botcom.channel_current, 'say', "Nope. %s has a permanent claim on %s!" % (str(bot.config.core.owner), target))
            return

        if bladder.percentnum < 10:
            osd(bot, botcom.channel_current, 'say', "You don't have enough pee in your bladder to make a valid claim!")
            return

        if bot_check_inlist(bot, target, [claimerdict["ownedby"]]) and claimerdict["ownedbyvalid"] == "valid":
            osd(bot, botcom.channel_current, 'action', "facepalms")
            osd(bot, botcom.channel_current, 'say', "You can't claim " + target + ", " + botcom.instigator + ". They already have a claim on you.")
            return

        if bot_check_inlist(bot, target, ["everyone"]):
            osd(bot, botcom.channel_current, 'say', botcom.instigator + " couldn't decide where to aim and pisses everywhere!")
            set_nick_value(bot, botcom.instigator, "long", 'claims', "bladder", time.time())
            return

        targetchecking = bot_target_check(bot, botcom, target, [])
        if not targetchecking["targetgood"]:
            return osd(bot, botcom.channel_current, 'say', targetchecking["error"])
        target = nick_actual(bot, target)

        bladdermessage = []

        claimeedict = get_nick_claims(bot, target)

        if not claimeedict["ownedby"]:
            bladdermessage.append("Claimed!")
        elif bot_check_inlist(bot, botcom.instigator, [claimeedict["ownedby"]]):
            if claimeedict["ownedbyvalid"] == "expired":
                bladdermessage.append("The claim has been renewed!")
            elif claimeedict["ownedbyvalid"] == "valid":
                return osd(bot, botcom.channel_current, 'say', botcom.instigator + ", you already claimed " + target + "!")
            else:
                bladdermessage.append("The claim has been renewed!")
        elif not bot_check_inlist(bot, botcom.instigator, [claimeedict["ownedby"]]):
            if claimeedict["ownedbyvalid"] == "expired":
                bladdermessage.append("The claim has been stolen from " + claimeedict["ownedby"] + "!")
            elif claimeedict["ownedbyvalid"] == "valid":
                return osd(bot, botcom.channel_current, 'say', target + " has already been claimed by " + str(claimeedict["ownedby"]) + ", so back off!")
            else:
                bladdermessage.append("The claim has been stolen from " + claimeedict["ownedby"] + "!")
        else:
            bladdermessage.append("Claimed!")

        bladdermessage.insert(0, botcom.instigator + " releases the contents of their bladder on " + target + "!")

        osd(bot, botcom.channel_current, 'say', bladdermessage)

        # set the claims
        duration = randint(claim_gamedict["durationmin"], claim_gamedict["durationmax"])
        duration = duration * (bladder.timesince / claim_gamedict["fullbladderseconds"])
        set_nick_claims(bot, botcom.instigator, target, duration)


def set_nick_claims(bot, nickclaimer, nickclaimee, duration):

    nickclaimer, nickclaimee = str(nickclaimer), str(nickclaimee)

    # set claimer ownership on claimee
    claimeedict = get_nick_claims(bot, nickclaimee)
    claimeedict["ownedby"] = nickclaimer

    # calculate duration of claim
    claimeedict["ownedbytime"] = time.time() + duration

    claimeedict["ownedbyvalid"] = "valid"

    set_nick_value(bot, nickclaimee, "long", 'claims', "claimdict", claimeedict)

    # set claimer ownership
    claimerdict = get_nick_claims(bot, nickclaimer)
    if nickclaimee not in claimerdict["ownings"]:
        claimerdict["ownings"].append(nickclaimee)
    set_nick_value(bot, nickclaimer, "long", 'claims', "claimdict", claimerdict)

    # empty bladder
    set_nick_value(bot, nickclaimer, "long", 'claims', "bladder", time.time())


def get_nick_claims(bot, nick):

    claimdict = get_nick_value(bot, nick, "long", 'claims', "claimdict") or None
    if not claimdict or not isinstance(claimdict, dict):
        claimdict = dict()
        set_nick_value(bot, nick, "long", 'claims', "claimdict", claimdict)

    if "ownedby" not in claimdict.keys():
        claimdict["ownedby"] = None

    if "ownedbyvalid" not in claimdict.keys():
        claimdict["ownedbyvalid"] = "expired"

    if "ownedbytime" not in claimdict.keys():
        claimdict["ownedbytime"] = 0

    # expired claims
    if not claimdict["ownedbytime"]:
        claimdict["ownedbytime"] = 0
    timesinceclaim = claimdict["ownedbytime"] - time.time()
    if timesinceclaim <= 0:
        claimdict["ownedbyvalid"] = "expired"

    if "ownings" not in claimdict.keys():
        claimdict["ownings"] = []

    for claimnick in claimdict["ownings"]:
        tempcheckdict = get_nick_value(bot, claimnick, "long", 'claims', "claimdict") or None
        if not tempcheckdict or not isinstance(tempcheckdict, dict):
            tempcheckdict = dict()
            set_nick_value(bot, claimnick, "long", 'claims', "claimdict", tempcheckdict)
        if "ownedbytime" not in tempcheckdict.keys():
            tempcheckdict["ownedbytime"] = 0
        if not tempcheckdict["ownedbytime"]:
            tempcheckdict["ownedbytime"] = 0
        timesinceclaim = tempcheckdict["ownedbytime"] - time.time()
        if timesinceclaim <= 0:
            tempcheckdict["ownedbyvalid"] = "expired"
        set_nick_value(bot, claimnick, "long", 'claims', "claimdict", tempcheckdict)

    set_nick_value(bot, nick, "long", 'claims', "claimdict", claimdict)

    return claimdict


def get_nick_bladder(bot, nick):

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
    bladder.percentnum = int(str(bladder.percent).split("%")[0])
    bladder.lastpeedisp = str(str(humanized_time(bladder.timesince) + " ago"))

    return bladder
