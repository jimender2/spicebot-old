import sopel.module
import sqlite3
from sopel.tools.target import User, Channel
from random import randint

@sopel.module.require_admin
@sopel.module.commands('getcmd')
def get_tables(bot, trigger):
    bot.say(trigger.group(1))
