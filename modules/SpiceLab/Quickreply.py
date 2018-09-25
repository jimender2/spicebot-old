import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# author deathbybandaid


dontsaylist = ['offend', 'offended', 'offense', 'offensive']


@rule('(.*)')
@sopel.module.thread(True)
def offensedetect(bot, trigger):

    # does not apply to bots
    if trigger.nick.lower() in bot_config_names(bot):
        return

    if not str(spicemanip(bot, trigger, 1)).startswith("."):
        return

    if str(spicemanip(bot, trigger, 1).lower().replace(".", "")) in dontsaylist:
        bot.say("success")
