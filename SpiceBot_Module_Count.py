import sopel.module
import os
import sys
from os.path import exists
import fnmatch

dirpath = os.path.dirname(__file__)

@sopel.module.rate(120)
@sopel.module.commands('modulecount')
def modulecount(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        modulecount = str(len(fnmatch.filter(os.listdir(dirpath), '*.py')))
        bot.say('There are currently ' + modulecount +' custom modules installed.')

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
