import sopel.module
import os
import sys
from os.path import exists

script_dir = os.path.dirname(__file__)

@sopel.module.require_admin
@sopel.module.require_privmsg
@sopel.module.commands('spicebotadmin')
def spicebotreloadadmin(bot, trigger):
    for c in bot.channels:
        channel = c
    options = str("update, restart")
    service = bot.nick.lower()
    if not trigger.group(2):
        bot.say("Which Command Do You want To run?")
        bot.say("Options Are: " + options)
    else:
        commandused = trigger.group(2)
        if commandused == 'update':
            bot.msg(channel, trigger.nick + " Commanded me to update from Github and restart. Be Back Soon!")
            update(bot, trigger)
            restart(bot, trigger)
        elif commandused == 'restart':
            bot.msg(channel, trigger.nick + " Commanded me to restart. Be Back Soon!")
            restart(bot, trigger)
    
def restart(bot, trigger):
    bot.say('Restarting Service...')
    os.system("sudo service " + str(service) + " restart")
    bot.say('If you see this, the service is hanging. Run Command Again.')

def update(bot, trigger):
    bot.say('Pulling From Github...')
    os.system("sudo git -C " + script_dir + " pull")
    bot.say('Cleaning Directory...')
    os.system("sudo rm " + script_dir + "/*.pyc")
