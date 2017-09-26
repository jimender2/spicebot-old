import sopel.module
from sopel.module import OP
from sopel.tools.target import User, Channel

@sopel.module.commands('isop')
def isop(bot,trigger):
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

@sopel.module.commands('getpriv')
def getpriv(bot,trigger):
    if not trigger.group(2):
        nick = trigger.nick.lower()
    else:
        nick = trigger.group(2).lower()
    priv = str(bot.channel[trigger.sender][nick])
    bot.say(priv)
