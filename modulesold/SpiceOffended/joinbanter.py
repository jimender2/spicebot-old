import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# author deathbybandaid


# watch Joins
@event('JOIN')
@rule('.*')
@sopel.module.thread(True)
def joindetect(bot, trigger):

    # does not apply to bot
    if trigger.nick.lower() == bot.nick.lower():
        return

    if "join_offend_check" not in bot.memory:
        bot.memory["join_offend_check"] = []

    if trigger.nick in bot.memory["join_offend_check"]:
        return

    bot.say("Who invited " + trigger.nick + " to " + trigger.sender + "?")
    bot.memory["join_offend_check"].append(trigger.nick)


# Startup check
@sopel.module.interval(5)
def startupcheck(bot):

    if "startup_offend_check" in bot.memory:
        return
    bot.memory["startup_offend_check"] = True

    # possibly in more than one channel
    for channel in bot.channels:
        bot.msg(channel, "Look at all the worthless fleshbags lurking in " + channel + "! Disgusting.")
