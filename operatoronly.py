import sopel.module
from sopel.module import commands, example, OP

@sopel.module.commands('optest')
def optest(bot,trigger):
    if str(trigger.nick) < str(OP):
        bot.say('you are op')
    else:
        bot.say("you are not op")
