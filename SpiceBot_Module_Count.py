import sopel.module
import sys
import os
from os.path import exists
import fnmatch
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('modulecount')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    modulecount = str(len(fnmatch.filter(os.listdir(moduledir), '*.py')))
    bot.say('There are currently ' + modulecount +' custom modules installed.')
