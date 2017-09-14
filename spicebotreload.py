import sopel.module
import os
import sys

@sopel.module.commands('spicebotreload')
def spicebotreload(bot, trigger):
  os.system("sh reload.sh")
