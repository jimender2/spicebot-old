import sopel.module
import os
import sys
from os.path import exists

script_dir = os.path.dirname(__file__)

@sopel.module.require_admin
@sopel.module.require_privmsg
@sopel.module.commands('pipinstall')
def pipinstall(bot, trigger):
    if not trigger.group(2):
        bot.say("You must specify a pip package")
    else:
        bot.say("attempting to install " + trigger.group(2))
        os.system("sudo pip install " + trigger.group(2))
        bot.say('Possibly done installing')
