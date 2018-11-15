import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('opersonly')
def mainfunction(bot, trigger):
    return startupcheck(bot, False)


# watch Joins
@event('JOIN')
@rule('.*')
@sopel.module.thread(True)
def joindetect(bot, trigger):

    # does not apply to bot
    if trigger.nick.lower() == bot.nick.lower():
        return

    # give chanserv time to OP
    time.sleep(5)

    # If new person not OP, kick
    if not bot.privileges[trigger.sender.lower()][trigger.nick.lower()] >= module.OP:
        # make sure bot is OP
        if bot.privileges[trigger.sender.lower()][bot.nick.lower()] >= module.OP:
            bot.write(['KICK', trigger.sender, trigger.nick], "You are not authorized to join " + trigger.sender)
        else:
            bot.say("I need to be OP to kick unauthorized users such as " + trigger.nick + " from " + trigger.sender)


# Startup check
@sopel.module.interval(5)
def startupcheck(bot, autorun=True):

    if "startup_op_check" in bot.memory and autorun:
        return
    if autorun:
        bot.memory["startup_op_check"] = True

    # possibly in more than one channel
    for channel in bot.channels:

        bot.msg(channel, "Running Oper privacy sweep for  " + channel)
        if not bot.privileges[channel.lower()][bot.nick.lower()] >= module.OP:
            bot.msg(channel, "I need to be OP to kick unauthorized users from " + channel)
            pass

        for user in bot.privileges[channel.lower()].keys():
            if user.lower() != bot.nick.lower():
                if not bot.privileges[channel.lower()][user.lower()] >= module.OP:
                    bot.write(['KICK', channel, user], "You are not authorized to join " + channel)
