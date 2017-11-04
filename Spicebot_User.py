import sopel.module
import os
import sys
import fnmatch
from os.path import exists
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('spicebot')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    for c in bot.channels:
        channel = c
    options = str("warn, channel, modulecount, owner, github")
    if not trigger.group(2):
        bot.say("That's my name. Don't wear it out!")
    else:
        commandused = trigger.group(2)
        if commandused == 'warn':
            bot.msg(channel, "This is just a warning. Overuse of the bot, can get you kicked or banned by an operator. If you want to purely play with the bot, go to ##SpiceBotTest, or send Spicebot a PrivateMessage.")
        elif commandused == 'channel':
            bot.say("You can find me in " + channel)
        elif commandused == 'modulecount':
            modulecount = str(len(fnmatch.filter(os.listdir(moduledir), '*.py')))
            bot.say('There are currently ' + modulecount +' custom modules installed.')
        elif commandused == 'owner':
            bot.say(bot.config.core.owner)
        elif commandused == 'github':
            bot.say('Spiceworks IRC Modules     https://github.com/deathbybandaid/sopel-modules')
