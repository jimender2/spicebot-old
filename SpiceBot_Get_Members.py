import sopel.module
import sqlite3
from sopel.tools.target import User, Channel
from random import randint

@sopel.module.require_admin
@sopel.module.commands('getmembers')
def getMembers(bot,trigger):
    #users = str(bot.channels[trigger.sender].users)
    #bot.say(users)
    userlist = []
    for u in bot.channels[trigger.sender].users:
        bot.say(u)
        userlist.append(u)
    randno = randint(0,len(userlist))
    randUser = userlist[randno]
    bot.say('Here is a randomly picked user: ' + randUser)
