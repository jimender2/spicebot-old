import sopel.bot
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

def get_botname(bot):
    botname = bot.nick
    return botname

botname = get_botname(bot)

@sopel.module.commands('botname')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    bot.say(str(botname) + ' test')
