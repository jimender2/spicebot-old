import sopel.module
import sqlite3
from sopel.tools.target import User, Channel
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.require_admin
@sopel.module.commands('getmembers')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    userlist = []
    for u in bot.channels[trigger.sender].users:
        bot.say(u)
        userlist.append(u)
    randno = randint(0,len(userlist))
    randUser = userlist[randno]
    bot.say('Here is a randomly picked user: ' + randUser)
