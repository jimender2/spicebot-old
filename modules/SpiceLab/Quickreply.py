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
                            "type": "target",
                            "reply": "Testing Beta on $target",
                            }
                }


@rule('(.*)')
@sopel.module.thread(True)
def watchallthethings(bot, trigger):

    # modcom dynamic Class
    modcom = class_create('modcom')
    modcom.default = 'modcom'

    # open global dict as part of modcom class
    global commandsdict
    modcom.gamedict = commandsdict

    # does not apply to bots
    if trigger.nick.lower() in bot_config_names(bot):
        return

    if not str(spicemanip(bot, trigger, 1)).startswith("."):
        return

    modcom.triggerargsarray = spicemanip(bot, trigger, 'create')
    modcom.dotcommand = spicemanip(bot, modcom.triggerargsarray, 1).lower().replace(".", "")
    modcom.triggerargsarray = spicemanip(bot, modcom.triggerargsarray, '2+')

    if dotcommand not in modcom.commandsdict.keys():
        osd(bot, trigger.sender, 'say', "I don't seem to have a command for " + modcom.dotcommand)
        return

    modcom.commandtype = modcom.commandsdict[modcom.dotcommand]["type"]

    command_function_run = str('botfunction_' + modcom.commandtype + '(bot, trigger, modcom)')
    eval(command_function_run)


def botfunction_simple(bot, trigger, modcom):
    reply = modcom.commandsdict[modcom.dotcommand]["reply"]
    osd(bot, trigger.sender, 'say', reply)


def botfunction_target(bot, trigger, modcom):

    target = spicemanip(bot, modcom.triggerargsarray, 1)
    if not target:
        osd(bot, trigger.sender, 'say', "No target provided")
        return

    reply = modcom.commandsdict[modcom.dotcommand]["reply"].replace("$target", target)
    osd(bot, trigger.sender, 'say', reply)
