import sopel.module
import os
import sys
from os.path import exists
from inspect import currentframe, getframeinfo
from pathlib import Path

script_dir = os.path.dirname(__file__)
filename = getframeinfo(currentframe()).filename
script_dirname = str(str(Path(filename).resolve().parent).split("/", 1)[1]).split("/", 1)[1]

@sopel.module.require_admin
@sopel.module.require_privmsg
@sopel.module.commands('spicebotreload')
def spicebotreload(bot, trigger):
  if str(script_dirname) == 'github':
    version = 'master'
    service = 'spicebot'
  elif str(script_dirname) == 'githubdev':
    version = 'dev'
    service = 'spicebotdev'
  
  bot.say('Pulling From Github ' + version)
  os.system("sudo git -C " + script_dir + " pull")
  bot.say('Cleaning Directory.')
  os.system("sudo rm " + script_dir + "/*.pyc")
  bot.say('Restarting Service')
  os.system("sudo service " + service + " restart")
