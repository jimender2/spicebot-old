import sopel.module
import os
import sys
from os.path import exists
import git
import shutil

DIR_NAME = os.path.dirname(__file__)
repo = git.Repo.init(script_dir)
REMOTE_URL = "https://github.com/deathbybandaid/sopel-modules.git"

@sopel.module.require_admin
@sopel.module.commands('spicebotreload')
def spicebotreload(bot, trigger):
  bot.say('Pulling From Github')
  if os.path.isdir(DIR_NAME):
    origin = repo.create_remote('origin',REMOTE_URL)
    origin.pull(origin.refs[0].remote_head)
  else
    bot.say('Git directory is NOT present.')
  
  bot.say('Restarting Service')
  os.system("sudo service sopel restart")
