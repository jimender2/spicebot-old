from sopel import module
import datetime
import sys

@sopel.module.rate(120)
def humpdaybot(bot,trigger):
    whatistoday = str(datetime.datetime.today().weekday())        
    wednesdaynumber = '2'
    if whatistoday == wednesdaynumber:
        bot.say("Today is Wednesday, AKA HUMPDAY!!!!")
    else:
        bot.say("Today is not humpday.")
humpdaybot.commands = ['humpday']
