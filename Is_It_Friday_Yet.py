import sopel.module
import datetime
import sys

@sopel.module.rate(120)
@sopel.module.commands('isitfriday','isitfridayyet')
def fridaybot(bot,trigger):
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
