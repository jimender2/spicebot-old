import sopel.module
import os
import sys
from os.path import exists
import fnmatch

dirpath = os.path.dirname(__file__)

@sopel.module.commands('modulecount')
def modulecount(bot,trigger):
    modulecount = str(len(fnmatch.filter(os.listdir(dirpath), '*.py')))
    bot.say('There are currently ' + modulecount +' custom modules installed.')
