# http://dilbert.com/search_results?terms=cats
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2


@sopel.module.commands('nofun','!fun')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'nofun')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, 0)
    if not target:
        message = "But... but .... that's no fun."
    else:
        message = "That's no fun " + target
    osd(bot, trigger.sender, 'say', str(message))
