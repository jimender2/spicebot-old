import sopel.module
import sys
import datetime

@sopel.module.commands('isitfriday','isitfridayyet')
def isitfriday(bot,trigger):
    whatistoday = str(datetime.datetime.today().weekday())        
    fridaynumber = '4'
    if whatistoday == fridaynumber:
        bot.say("TGIF! It's finally here!!!")
    elif whatistoday == '5' or whatistoday == '6':
        bot.say("It's the Weekend. It should be better than Friday!")
    else:
        daysmath = int(fridaynumber) - int(whatistoday)
        bot.say("Unfortunately Friday is " + daysmath + " away. I'm sure we'll make it there!")
