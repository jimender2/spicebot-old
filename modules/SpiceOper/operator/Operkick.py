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

    if not bot.privileges[trigger.sender.lower()][trigger.nick.lower()] >= module.OP and bot.privileges[trigger.sender.lower()][bot.nick.lower()] >= module.OP:
        bot.write(['KICK', trigger.sender, trigger.nick], "You are not authorized to join " + trigger.sender)
