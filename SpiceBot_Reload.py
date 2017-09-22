import sopel.module
import os
import sys
from os.path import exists

script_dir = os.path.dirname(__file__)

@sopel.module.require_admin
@sopel.module.require_privmsg
@sopel.module.commands('spicebotreload')
def spicebotreload(bot, trigger):
  bot.say('Pulling From Github')
  os.system("sudo git -C " + script_dir + " pull")
  bot.say('Cleaning Directory.')
  os.system("sudo rm" + script_dir + "/*.pyc")
  bot.say('Restarting Service')
  os.system("sudo service sopel restart")
