import sopel.module
import sqlite3
from sopel.tools.target import User, Channel
from random import randint

@sopel.module.require_admin
@sopel.module.commands('dbtest')
def get_tables(bot, trigger):
    con = bot.db.connect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM nick_ids;")
    bot.say(str(cursor.fetchall()))
