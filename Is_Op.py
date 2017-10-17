import sopel.module
from sopel.module import OP
from sopel.tools.target import User, Channel

@sopel.module.commands('isop')
def isop(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if not trigger.group(2):
            nick = trigger.nick.lower()
        else:
            nick = trigger.group(2).lower()
        try:    
            if bot.privileges[trigger.sender][nick] == OP:
                bot.say(nick + ' is an op.')
            else: 
                bot.say(nick + ' is not an op.')
        except KeyError:
            bot.say(nick + ' is not here right now!')

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
