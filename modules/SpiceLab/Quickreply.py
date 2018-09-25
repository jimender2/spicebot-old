import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# author deathbybandaid


argslist = ['testa', 'testb', 'testc', 'testd']


commandsdict = {
                "testa": "Testing alpha",
                "testb": "testing beta",
                "testc": "testing gamma",
                "testd": "testering delta",
                }


@rule('(.*)')
@sopel.module.thread(True)
def watchallthethings(bot, trigger):

    global commandsdict

    # does not apply to bots
    if trigger.nick.lower() in bot_config_names(bot):
        return

    if not str(spicemanip(bot, trigger, 1)).startswith("."):
        return

    dotcommand = str(spicemanip(bot, trigger, 1).lower().replace(".", ""))

    if dotcommand in commandsdict.keys():
        bot.say(str(commandsdict[dotcommand]))
    else:
        bot.say("I don't seem to have a command for " + str(spicemanip(bot, trigger, 1)))
