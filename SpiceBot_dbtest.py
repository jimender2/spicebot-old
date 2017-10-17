import sopel.module
import sqlite3
from sopel.tools.target import User, Channel
from random import randint

@sopel.module.require_admin
@sopel.module.commands('dbtest')
def get_tables(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        con = bot.db.connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM nick_ids;")
        bot.say(str(cursor.fetchall()))
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
