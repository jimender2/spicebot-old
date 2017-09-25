import sopel.module
from sopel.module import commands, example, OP

@sopel.module.commands('optest')
def optest(bot,trigger):
    if trigger.isop:
        bot.say('you are op')
    elif not trigger.isop:
        bot.say('you are not op')
    else:
        bot.say("this does not work")
