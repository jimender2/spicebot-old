import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *


@event('JOIN')
@rule('.*')
@sopel.module.thread(True)
def joindetect(bot, trigger):

    # give chanserv time to OP
    time.sleep(5)

    # If new person not OP, kick
    if not bot.privileges[trigger.sender.lower()][trigger.nick.lower()] >= module.OP:
        # make sure bot is OP
        if bot.privileges[trigger.sender.lower()][bot.nick.lower()] >= module.OP:
            bot.write(['KICK', trigger.sender, trigger.nick], "You are not authorized to join " + trigger.sender)
        else:
            bot.say("I need to be OP to kick unauthorized users such as " + trigger.nick + " from " + trigger.sender)
