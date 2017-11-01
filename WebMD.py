import sopel.module
import sopel
from sopel import module, tools
import random
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.commands('webmd','webmdadd','webmddel')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    commandtrimmed = trigger.group(1)
    commandtrimmed = str(commandtrimmed.split("webmd", 1)[1])
    webmd = get_webmd(bot)
    if commandtrimmed == '':
        target = trigger.group(3) or trigger.nick
        responses  = ["has died from","is being treated for","is recovering from"]
        reply = random.randint(0,len(responses) - 1)
        condition = str(responses [reply])
        try:
            result =random.choice(webmd)
        except IndexError:
            result = "death"
        conclusion = str(target + ' ' + condition + ' ' + result + '.')
        bot.say(conclusion)
    elif not trigger.group(2):
        bot.say("What would you like to add/remove?")
    else:
        webmdchange = str(trigger.group(2))
        if commandtrimmed == 'add':
            if webmdchange in webmd:
                bot.say(webmdchange + " is already in the webmd locker.")
                rescan = 'False'
            else:
                webmd.append(webmdchange)
                update_webmd(bot, webmd)
                rescan = 'True'
        elif commandtrimmed == 'del':
            if webmdchange not in webmd:
                bot.say(webmdchange + " is not in the webmd locker.")
                rescan = 'False'
            else:
                webmd.remove(webmdchange)
                update_webmd(bot, webmd)
                rescan = 'True'
        if rescan == 'True':
            webmd = get_webmd(bot)
            if webmdchange in webmd:
                bot.say(webmdchange + " has been added to the webmd locker.")
            else:
                bot.say(webmdchange + ' has been removed from the webmd locker.')

def get_webmd(bot):
    for channel in bot.channels:
        webmd = bot.db.get_nick_value(channel, 'webmd_locker') or []
        return webmd
        
def update_webmd(bot, webmd):
    for channel in bot.channels:
        bot.db.set_nick_value(channel, 'webmd_locker', webmd)
