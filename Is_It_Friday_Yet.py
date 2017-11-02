import sopel.module
import datetime
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('isitfriday','isitfridayyet')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    whatistoday = str(datetime.datetime.today().weekday())        
    fridaynumber = '4'
    if whatistoday == fridaynumber:
        bot.say("TGIF! It's finally here!!!")
    elif whatistoday == '5' or whatistoday == '6':
        bot.say("It's the Weekend. It should be better than Friday!")
    else:
        daysmath = int(fridaynumber) - int(whatistoday)
        if daysmath == int('1'):
            bot.say("Unfortunately Friday is " + str(daysmath) + " day away. I'm sure we'll make it there!")
        else:
            bot.say("Unfortunately Friday is " + str(daysmath) + " days away. I'm sure we'll make it there!")
