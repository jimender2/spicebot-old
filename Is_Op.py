import sopel.module
from sopel.module import OP

@sopel.module.commands('isop')
def optest(bot,trigger):
    if bot.privileges[trigger.sender][trigger.nick] == OP:
        bot.say('you are op')
    elif bot.privileges[trigger.sender][trigger.nick] < OP:
        bot.say('you are not op')
    else:
        bot.say("this does not work")
