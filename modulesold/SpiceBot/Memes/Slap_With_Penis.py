#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

penistypes = ["Venezuelan Beaverpenis", "penis", "Ocean Sunpenis", "Blobpenis", "Oyster Toadpenis",
              "Slippery Dick", "Humuhumunukunukuāpuaʻa", "Giant Goliath Tiger penis", "Red-lipped Batpenis", "Suckermouth Catpenis",
              "Collared Carpetshark", "Naked-back Knifepenis"]
vowels = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')


@sopel.module.commands('penis', 'dickslap')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'penis')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Slap some bitch with a penis."""
    target = spicemanip(bot, triggerargsarray, 1)
    reason = spicemanip(bot, triggerargsarray, '2+')
    message = "Whoops, something went wrong."
    penistype = spicemanip(bot, penistypes, 'random')
    penismsg = "a " + penistype
    # Vowel awareness
    if penistype.startswith(vowels):
        penismsg = "an " + penistype

    # No target specified
    if not target:
        message = "You haven't told me who or what you want to slap, you moron."

    # Can't slap the bot
    if target == bot.nick:
        message = "Get fucked, that's not gonna happen."

    # Target is fine
    else:
        if not reason:
            message = trigger.nick + " slaps " + target + " with " + penismsg + "."
        else:
            if reason.startswith('for ') or reason.startswith('because ') or reason.startswith('cause '):
                message = trigger.nick + " slaps " + target + " with " + penismsg + " " + reason + "."
            else:
                message = trigger.nick + " slaps " + target + " with " + penismsg + " for " + reason + "."

    osd(bot, trigger.sender, 'say', message)
