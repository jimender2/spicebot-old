import sopel.module
from sopel.module import ADMIN
from sopel.tools.target import User, Channel

@sopel.module.commands('isadmin')
def isadmin(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if not trigger.group(2):
            if trigger.admin:
                bot.say(trigger.nick + ' is an admin')
            else:
                bot.say(trigger.nick + ' is not an admin')
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
