import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

bemoreofapussy = [
                    "Would you like a tissue?",
                ]


@rule('(.*)')
@sopel.module.thread(True)
def offensedetect(bot, trigger):

    # does not apply to bots
    if trigger.nick.lower() in bot_config_names(bot):
        return

    triggerargsarray = spicemanip(bot, trigger, 'create')
    if spicemanip(bot, triggerargsarray, 1).lower() == 'that':

        osd(bot, channeltarget, 'say', str(spicemanip(bot, bemoreofapussy, 'random')))
