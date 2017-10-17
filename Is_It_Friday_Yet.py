import sopel.module
import datetime
import sys

@sopel.module.rate(120)
@sopel.module.commands('isitfriday','isitfridayyet')
def fridaybot(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
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
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
