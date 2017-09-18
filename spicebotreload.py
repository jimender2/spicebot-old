import sopel.module
import os
import sys
from os.path import exists

script_dir = os.path.dirname(__file__)

@sopel.module.require_admin
@sopel.module.commands('spicebotreload')
def spicebotreload(bot, trigger):
  os.system("sudo git -C " + script_dir + " pull")
  os.system("sudo service sopel restart")
