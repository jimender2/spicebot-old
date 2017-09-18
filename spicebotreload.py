import sopel.module
import os
import sys
from os.path import exists
import git

git_dir = os.path.dirname(__file__)
g = git.cmd.Git(git_dir)

@sopel.module.require_admin
@sopel.module.commands('spicebotreload')
def spicebotreload(bot, trigger):
  bot.say('Pulling From Github')
  g.pull()
  bot.say('Restarting Service')
  os.system("sudo service sopel restart")
