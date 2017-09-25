import sopel.module
from __future__ import print_function
from sopel.module import rule, event, commands, example, OP
from collections import deque

@sopel.module.commands('optest')
def optest(bot,trigger):
    if trigger.isop:
        bot.say('you are op')
    elif not trigger.isop:
        bot.say('you are not op')
    else:
        bot.say("this does not work")
