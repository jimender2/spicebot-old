import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

startupinterval = 5


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
@sopel.module.interval(startupinterval)
def startupcheck(bot):

    # possibly in more than one channel
    for channel in bot.channels:

        kicklist = []
        for user in bot.privileges[channel.lower()].keys():
            if user.lower() != bot.nick.lower():
                if not bot.privileges[channel.lower()][user.lower()] >= module.OP:
                    kicklist.append(user)

        # empty list
        if kicklist == []:
            return

        # make sure bot is OP
        if bot.privileges[channel.lower()][bot.nick.lower()] >= module.OP:
            for user in kicklist:
                bot.write(['KICK', channel, user], "You are not authorized to join " + channel)
        else:
            bot.msg(channel, "I need to be OP to kick unauthorized users such as " + spicemanip(bot, kicklist, 'list') + " from " + channel)

    # don't check for a while
    startupinterval = 9999999999999999999999999999999999
