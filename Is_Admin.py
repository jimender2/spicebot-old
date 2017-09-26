import sopel.module
from sopel.module import ADMIN
from sopel.tools.target import User, Channel

@sopel.module.commands('isadmin')
def isadmin(bot,trigger):
    if not trigger.group(2):
        nickame = trigger.nick.lower()
        if nickame.admin:
            bot.say(trigger.nick + ' is an admin')
        else:
            bot.say(trigger.nick + ' is not an admin')
