import sopel.module
from sopel.module import commands, example, OP

@sopel.module.commands('optest')
def optest(bot,trigger):
    if trigger.nick == OP:
        bot.say('you are op')
    else:
        bot.say("you are not op")
