import sopel.module
import datetime
import sys

@sopel.module.rate(120)
@sopel.module.commands('monday','mondays','fuckmonday','fuckmondays','tuesday','tuesdays','fucktuesday','fucktuesdays','wednesday','wednesdays','fuckwednesday','fuckwednesdays','thursday','thursdays','fuckthursday','fuckthursdays','friday','fridays','fuckfriday','fuckfridays','saterday','saterdays','fucksaturday','fucksaturdays','sunday','sundays','fucksunday','fucksundays')
def daybot(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        whichtrig = trigger.group(1)
    
        if whichtrig.endswith('s'):
            whichtrig = whichtrig[:-1]
    
        if whichtrig.endswith('monday'): 
            whichtrigday = 'Monday'
        elif whichtrig.endswith('tuesday'): 
            whichtrigday = 'Tuesday'
        elif whichtrig.endswith('wednesday'): 
            whichtrigday = 'Wednesday'
        elif whichtrig.endswith('thursday'): 
            whichtrigday = 'Thursday'
        elif whichtrig.endswith('friday'): 
            whichtrigday = 'Friday'
        elif whichtrig.endswith('saturday'): 
            whichtrigday = 'Saturday'
        elif whichtrig.endswith('sunday'): 
            whichtrigday = 'Sunday'    
        else:
            whichtrigday = 'null'
     
        if whichtrig.startswith('fuck'):
            whichtrigmood = 'salty'
        else:
            whichtrigmood = 'null'
    
        whatistoday = str(datetime.datetime.today().weekday())
        if whatistoday == '0':
            today = "Monday"
        elif whatistoday == '1':
            today = "Tuesday"
        elif whatistoday == '2':
            today = "Wednesday"
        elif whatistoday == '3':
            today = "Thursday"
        elif whatistoday == '4':
            today = "Friday"
        elif whatistoday == '5':
            today = "Saturday"
        elif whatistoday == '6':
            today = "Sunday"
    
        if whichtrigmood == 'salty':
            if whichtrigday == today:
                bot.say(today + "s " + "really do suck!")
            else:
                bot.say(whichtrigday + "s " + "sometimes do suck!")
        else:
            if today == whichtrigday:
                bot.say("Today is " + today + ", what about it?")
            else:
                bot.say(whichtrigday + ", what about it?")
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
