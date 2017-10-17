import sopel.module
import datetime
import sys

@sopel.module.rate(120)
@sopel.module.commands('humpday')
def humpdaybot(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        whatistoday = str(datetime.datetime.today().weekday())        
        wednesdaynumber = '2'
        if whatistoday == wednesdaynumber:
            bot.say("Today is Wednesday, AKA HUMPDAY!!!!")
        else:
            bot.say("Today is not humpday.")

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
