import sopel.module
from sopel.module import OP

@sopel.module.commands('isop')
def optest(bot,trigger):
    if bot.privileges[trigger.sender][trigger.nick] == OP:
        bot.say(trigger.nick + ', you are op.')
    elif bot.privileges[trigger.sender][trigger.nick] < OP:
        bot.say(trigger.nick + ', you are not op.')
