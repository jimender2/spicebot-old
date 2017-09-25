import sopel.module
from sopel.module import OP
from sopel.tools.target import User, Channel

@sopel.module.commands('isop')
def optest(bot,trigger):
    if not trigger.group(2):
        if bot.privileges[trigger.sender][trigger.nick] == OP:
            bot.say(trigger.nick + ', you are op.')
        elif bot.privileges[trigger.sender][trigger.nick] < OP:
            bot.say(trigger.nick + ', you are not op.')
    else:
        if trigger.group(2) in bot.channels:
            if bot.privileges[trigger.sender][trigger.group(2)] == OP:
                bot.say(trigger.group(2) + ' is op.')
            elif bot.privileges[trigger.sender][trigger.group(2)] < OP:
                bot.say(trigger.group(2) + ' is not op.')
        else:
            bot.say(trigger.group(2) + ' is not in this room.')
