# http://dilbert.com/search_results?terms=cats
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2

defaultoptions = [
    "I did not kill chat. (This time)",
    "Is it just me or is chat dead?",
    "What's the difference between a rear end kisser and a brown noser? Depth perception",
    "Doctor I need a new butt. Why?? Mine has a crack in it."
    ]


@sopel.module.commands('dead')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'dead')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    message = spicemanip(bot, defaultoptions, "random") or 'I did not kill chat. (This time)'
    osd(bot, trigger.sender, 'say', message)
