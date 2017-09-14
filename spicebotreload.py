import sopel.module
import os
import sys
from os.path import exists

script_dir = os.path.dirname(__file__)
rel_path = "reload.sh"
abs_file_path = os.path.join(script_dir, rel_path)

@sopel.module.require_admin
@sopel.module.commands('spicebotreload')
def spicebotreload(bot, trigger):
  os.system("sh " + abs_file_path)
