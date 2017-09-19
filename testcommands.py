import sopel.module
import sqlite3
from sopel.tools.target import User, Channel

@sopel.module.commands('getchannels')
def getChannels(bot,trigger):
	for c in bot.channels:
		bot.say("You can find me in " + c)
@sopel.module.commands('getmembers')
def getMembers(bot,trigger):
    #users = str(bot.channels[trigger.sender].users)
    #bot.say(users)
    for u in bot.channels[trigger.sender].users:
        bot.say(u)
@sopel.module.commands('dbtest')
def get_tables(bot, trigger):
    con = sqlite3.connect('sopel.db')
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    bot.say(str(cursor.fetchall()))
    
   
