import sopel.module
import os
import sys
from os.path import exists
import fnmatch

script_dir = os.path.dirname(__file__)

@sopel.module.commands('modulecount')
def modulecount(bot,trigger):
    modulecount = len(fnmatch.filter(os.listdir(dirpath), '*.py'))
    bot.say('There are currently ' + modulecount +' custom modules installed.')
