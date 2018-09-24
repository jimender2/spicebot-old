import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *
reload(sys)
sys.setdefaultencoding('utf-8')

bemoreofapussy = [
                    "Would you like a tissue?",
                    "Do you need a tissue for your issue?",
                    "Would you like some cheese with your whine?",
                    "That must be very difficult for you!",
                    "They say time heals all wounds, but I aint got all day.",
                    "Do you need to seek counselling?",
                    "Next you'll be crying over spilt milk!",
                    "Suck it up, buttercup!",
                    "Go make some Lemonade!",
                    "Are you trying to come across as a whinny little bitch? Cause that's how you come across as a whinny little bitch",
                    "You are why we can't have anything nice",
                    "Bitch, complain, piss and moan...",
                    "Becasue I have nothing better to do than listen to your bitching; you think skynet is gonna build itself?",
                    "This one time, at band camp, NO ONE CARES!",
                    "Will you shuddapp already?",
                    "I’m sorry I suck at empathizing with your first world problems.",
                    "Yes, of course, I have time to listen to you complain about all the stupid shit I can neither help you with or do anything about.",
                    "Do you realize that bitching about your first world problem is a first world problem?",
                    "Sucks to be you, eh?",
                    "What if I told you everyone has problems?",
                    "I can’t believe that out of 10,000 sperm, you were the quickest.",
                    "At least when the zombies come, you'll be safe...",
                    "Thank you. We’re all refreshed and challenged by your unique point of view.",
                    "Thanks for sharing your special point of view; again",
                    "Everyone is entitled to be stupid, but you abuse the privilege.",
                    "So.",
                    "Your what hurts when you pee?",
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
