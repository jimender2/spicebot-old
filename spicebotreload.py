import sopel.module
import os
import sys

@sopel.module.require_admin
@sopel.module.commands('spicebotreload')
def spicebotreload(bot, trigger):
  os.system("sh /home/pi/.sopel/github/reload.sh")
