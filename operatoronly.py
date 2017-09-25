import sopel.module
from sopel.module import rule, event, commands, example, OP
from collections import deque

@sopel.module.commands('optest')
def optest(bot,trigger):
    if trigger.privileges == OP:
        bot.say('you are op')
    elif not trigger.privileges == OP:
        bot.say('you are not op')
    else:
        bot.say("this does not work")
