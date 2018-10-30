import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# author deathbybandaid

valid_command_prefix = ['.', '!', ',']


# TODO a way to import stuff like this directly from other files?
# TODO redirect dict, this == that
commandsdict = {
                "testa": {
                            "type": "simple",
                            "reply": "This is a test of a quick reply to a command.",
                            },
                "testb": {
                            "type": "target",
                            "reply": "This is a target test directed at $target.",
                            },
                "testc": {
                            "type": "target",
                            "reply": "This is a target test directed at $target. Hopefully $target enjoys that kid of thing",
                            },
                "testd": {
                            "type": "test",
                            "reply": "grrrr",
                            },
                }


@rule('(.*)')
@sopel.module.thread(True)
def watcher(bot, trigger):
    if not str(trigger).startswith(tuple(valid_command_prefix)):
        return
    bot.say(str(trigger))


def watchallthethings(bot, trigger):

    # modcom dynamic Class
    modcom = class_create('modcom')
    modcom.default = 'modcom'

    # open global dict as part of modcom class
    global commandsdict
    modcom.commandsdict = commandsdict

    # does not apply to bots
    if trigger.nick.lower() in bot_config_names(bot):
        return

    # make sure first word starts with "."
    if not str(spicemanip(bot, trigger, 1)).startswith("."):
        return

    # create arg list
    modcom.triggerargsarray = spicemanip(bot, trigger, 'create')

    # command issued
    modcom.dotcommand = spicemanip(bot, modcom.triggerargsarray, 1).lower().replace(".", "")

    # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
    if not modcom.dotcommand:
        return

    # remainder, if any is the new arg list
    modcom.triggerargsarray = spicemanip(bot, modcom.triggerargsarray, '2+')

    # if there is nt a nested dictionary for the command requested, then privmsg and exit
    if modcom.dotcommand not in modcom.commandsdict.keys():
        return  # temp TODO
        osd(bot, trigger.sender, 'say', "I don't seem to have a command for " + modcom.dotcommand)
        return

    # execute function based on command type
    modcom.commandtype = modcom.commandsdict[modcom.dotcommand]["type"]
    command_function_run = str('botfunction_' + modcom.commandtype + '(bot, trigger, modcom)')
    try:
        eval(command_function_run)
    except NameError:
        osd(bot, trigger.sender, 'say', "This command is not setup with a proper 'type'.")


# Simple quick replies
def botfunction_simple(bot, trigger, modcom):
    reply = modcom.commandsdict[modcom.dotcommand]["reply"]
    osd(bot, trigger.sender, 'say', reply)


# Quick replies with a target person TODO use the targetfinder logic
def botfunction_target(bot, trigger, modcom):

    target = spicemanip(bot, modcom.triggerargsarray, 1)
    if not target:
        osd(bot, trigger.sender, 'say', "No target provided")
        return

    reply = modcom.commandsdict[modcom.dotcommand]["reply"].replace("$target", target)
    osd(bot, trigger.sender, 'say', reply)
