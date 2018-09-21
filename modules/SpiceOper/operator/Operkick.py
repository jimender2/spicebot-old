import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

allowedusers = ['under_score', 'DoubleD', 'deathbybandaid', 'dysonparkes']


@event('JOIN')
@rule('.*')
@sopel.module.thread(True)
def joindetect(bot, trigger):
    channel = trigger.sender
    instigator = trigger.nick

    if instigator not in allowedusers and bot.privileges[channel.lower()][bot.nick.lower()] >= module.OP:
        kicking = kicking_available(bot, channel)
        if kicking:
            bot.write(['KICK', channel, instigator], "You are not authorized for this channel")
