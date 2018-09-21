import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *


@rule('(.*)')
@sopel.module.thread(True)
def offensedetect(bot, trigger):

    triggerargsarray = spicemanip(bot, trigger, 'create')
    if [x for x in triggerargsarray if x in ['offended', 'offense']]:
        bot.say("kick")

    return
    # does not apply to bot
    if trigger.nick.lower() == bot.nick.lower():
        return

    # make sure bot is OP
    if bot.privileges[trigger.sender.lower()][bot.nick.lower()] >= module.OP:
        bot.write(['KICK', trigger.sender, trigger.nick], "You can't talk like that in " + trigger.sender)
    else:
        bot.say("I need to be OP to kick unauthorized users such as " + trigger.nick + " from " + trigger.sender + " for being offended.")
