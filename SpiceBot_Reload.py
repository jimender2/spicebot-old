import sopel.module
import os
import sys
from os.path import exists
from inspect import currentframe, getframeinfo
from pathlib import Path

script_dir = os.path.dirname(__file__)
service = os.path.split(os.getcwd())[1]

@sopel.module.require_admin
@sopel.module.require_privmsg
@sopel.module.commands('spicebotreload')
def spicebotreload(bot, trigger):
    bot.say(service)
    bot.say('Pulling From Github...')
    os.system("sudo git -C " + script_dir + " pull")
    bot.say('Cleaning Directory...')
    os.system("sudo rm " + script_dir + "/*.pyc")
    bot.say('Restarting Service...')
    os.system("sudo service " + str(service) + " restart")
    bot.say(' ')
    bot.say('If you see this, the service is hanging. Run Command Again.')
