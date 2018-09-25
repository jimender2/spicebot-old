import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# author deathbybandaid


commandsdict = {
                "testa": {
                            "type": "simple",
                            "reply": "Testing Alpha",
                            },
                "testb": {
                            "type": "target"
                            "reply": "Testing Beta on",
                            }
                }


@rule('(.*)')
@sopel.module.thread(True)
def watchallthethings(bot, trigger, commandsdict):

    # global commandsdict

    # does not apply to bots
    if trigger.nick.lower() in bot_config_names(bot):
        return

    if not str(spicemanip(bot, trigger, 1)).startswith("."):
        return

    triggerargsarray = spicemanip(bot, trigger, 'create')

    dotcommand = str(spicemanip(bot, triggerargsarray, 1).lower().replace(".", ""))
    triggerargsarray = spicemanip(bot, triggerargsarray, '2+')

    if dotcommand not in commandsdict.keys():
        osd(bot, trigger.sender, 'say', "I don't seem to have a command for " + dotcommand)
        return

    commandtype = str(commandsdict[dotcommand]["type"])

    command_function_run = str('botfunction_' + commandtype + '(bot, trigger, triggerargsarray, commandsdict)')
    eval(command_function_run)


def botfunction_simple(bot, trigger, triggerargsarray, commandsdict):
    osd(bot, trigger.sender, 'say', str(commandsdict[dotcommand]["reply"]))
    return


def botfunction_target(bot, trigger, triggerargsarray, commandsdict):
    osd(bot, trigger.sender, 'say', spicemanip(bot, triggerargsarray, 0).replace("$target", spicemanip(bot, triggerargsarray, 1)))
    return
