import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('warn','warning')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if not trigger.group(2):
        bot.say("This is just a warning. Overuse of the bot, can get you kicked or banned by an operator. If you want to purely play with the bot, go to ##SpiceBotTest, or send Spicebot a PrivateMessage.")
    elif not trigger.group(2) == bot.nick:
        bot.say(trigger.group(2).strip() + ", This is just a warning. Overuse of the bot, can get you kicked or banned by an operator. If you want to purely play with the bot, go to ##SpiceBotTest, or send Spicebot a PrivateMessage.")
