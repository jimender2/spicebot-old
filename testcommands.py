import sopel.module
import sqlite3
from sopel.tools.target import User, Channel

@sopel.module.require_admin
@sopel.module.commands('getchannels')
def getChannels(bot,trigger):
	for c in bot.channels:
		bot.say("You can find me in " + c)
@sopel.module.require_admin
@sopel.module.commands('getmembers')
def getMembers(bot,trigger):
    #users = str(bot.channels[trigger.sender].users)
    #bot.say(users)
    for u in bot.channels[trigger.sender].users:
        bot.say(u)
@sopel.module.require_admin
@sopel.module.commands('dbtest')
def get_tables(bot, trigger):
    con = bot.db.connect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM nick_ids;")
    bot.say(str(cursor.fetchall()))

@sopel.module.commands('getcmd')
def get_tables(bot, trigger):
    bot.say(trigger.group(1)
   
