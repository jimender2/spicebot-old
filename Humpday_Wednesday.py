import sopel.module
import datetime
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.commands('humpday')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    whatistoday = str(datetime.datetime.today().weekday())        
    wednesdaynumber = '2'
    if whatistoday == wednesdaynumber:
        bot.say("Today is Wednesday, AKA HUMPDAY!!!!")
    else:
        bot.say("Today is not humpday.")
