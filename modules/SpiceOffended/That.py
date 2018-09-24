import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

bemoreofapussy = [
                    "Would you like a tissue?",
                    "Do you need atissue for your issue?",
                    "Would you like some cheese with your whine?",
                    "That must be very difficult for you!",
                    "They say time heals all wounds, but I aint got all day.",
                    "Do you need to seek counsiling?",
                    "Next you'll be crying over spilt milk!",
                    "Suck it up, buttercup!",
                    "Go make some Lemonade!"
                ]


@module.rule('^(?:that)\s+?.*')
@sopel.module.thread(True)
def mainfunctionnobeguine(bot, trigger):

    # does not apply to bots
    if trigger.nick.lower() in bot_config_names(bot):
        return

    triggerargsarray = spicemanip(bot, trigger, 'create')
    if spicemanip(bot, triggerargsarray, 1).lower() == 'that':

        osd(bot, trigger.sender, 'say', str(spicemanip(bot, bemoreofapussy, 'random')))
