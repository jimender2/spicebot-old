# coding=utf-8
"""
lmgtfy.py - Sopel Let me Google that for you module
Copyright 2013, Dimitri Molenaars http://tyrope.nl/
Licensed under the Eiffel Forum License 2.
http://sopel.chat/
"""
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('lmgtfy', 'lmgify', 'gify', 'gtfy')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'lmgtfy')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger,triggerargsarray):
    """Let me just... google that for you."""
    #No input
    target = get_trigger_arg(bot,triggerargsarray,0)                                                     
    if not target:
        return bot.say('http://google.com/')
    bot.say('http://lmgtfy.com/?q=' + target.replace(' ', '+'))
