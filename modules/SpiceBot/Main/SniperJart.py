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


@sopel.module.commands('sniperjart', 'sjart')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'sniperjart')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Do the thing."""
    target = spicemanip(bot, triggerargsarray, 1)
    message = ""
    isvalid, validmsg = targetcheck(bot, botcom, target, instigator)
    if not target:
        message = trigger.nick + " orders a Jart™ with the unique scent of a SniperClif™ fart. DISCLAIMER: While it is quite potent, the SniperClif™ Jart™ is a short term scent. It might evoke a gag reflex and vomiting but, within 5 minutes, the scent has faded. It has also been known to bring on PTSD in people who have been removed from exposure for extended periods of time."
    elif isvalid == 0:
        message = "I'm not sure who to send this SniperClif™ Jart™ to."
    elif isvalid == 3:
        message = "Someone opened a SniperClif™ Jart™, that was truly disgusting!"
    else:
        message = trigger.nick + " sends a SniperClif™ Jart™ to " + target + "."
    osd(bot, trigger.sender, 'say', message)
