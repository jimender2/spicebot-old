import sopel.module
import datetime
import sys

@sopel.module.rate(120)
@sopel.module.commands('humpday')
def humpdaybot(bot,trigger):
    whatistoday = str(datetime.datetime.today().weekday())        
    wednesdaynumber = '2'
    if whatistoday == wednesdaynumber:
        bot.say("Today is Wednesday, AKA HUMPDAY!!!!")
    else:
        bot.say("Today is not humpday.")
