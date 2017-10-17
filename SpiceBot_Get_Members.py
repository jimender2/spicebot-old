import sopel.module
import sqlite3
from sopel.tools.target import User, Channel
from random import randint

@sopel.module.require_admin
@sopel.module.commands('getmembers')
def getMembers(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        #users = str(bot.channels[trigger.sender].users)
        #bot.say(users)
        userlist = []
        for u in bot.channels[trigger.sender].users:
            bot.say(u)
            userlist.append(u)
        randno = randint(0,len(userlist))
        randUser = userlist[randno]
        bot.say('Here is a randomly picked user: ' + randUser)
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
