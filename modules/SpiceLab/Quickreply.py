import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# author deathbybandaid


argslist = ['testa', 'testb', 'testc', 'testd']


@rule('(.*)')
@sopel.module.thread(True)
def offensedetect(bot, trigger):

    # does not apply to bots
    if trigger.nick.lower() in bot_config_names(bot):
        return

    if not str(spicemanip(bot, trigger, 1)).startswith("."):
        return

    if str(spicemanip(bot, trigger, 1).lower().replace(".", "")) in argslist:
        bot.say("success")
    else:
        bot.say("I don't seem to have a command for " + str(spicemanip(bot, trigger, 1)))
