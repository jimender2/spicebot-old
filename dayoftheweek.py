import sopel.module
import datetime

@sopel.module.commands('monday','fuckmonday','tuesday','fucktuesday','wednesday','fuckwednesday','thursday','fuckthursday','friday','fuckfriday','saterday','fucksaturday','sunday','fucksunday')
def daybot(bot, trigger):
    whichtrigday = whattriggerday()
    whichtrigmood = whattriggermood()
    today = whatdayisit()
    if whichtrigmood == 'salty':
        if whichtrigday == today:
            bot.say(today + "s " + "really do suck!")
        else:
            bot.say(whichtrigday + "s " + "sometimes do suck!")
    else:
        if today == whichtrigday:
            bot.say("Today is" + today + ", what about it?")
        else:
            bot.say(whichtrigday + ", what about it?")

def whatdayisit():
    whatistoday = str(datetime.datetime.today().weekday())
    bot.say(whatistoday + " is today")
    if whatistoday == '0':
        today = "monday"
    if whatistoday == '1':
        today = "tuesday"
    if whatistoday == '2':
        today = "wednesday"
    if whatistoday == '3':
        today = "thursday"
    if whatistoday == '4':
        today = "friday"
    if whatistoday == '5':
        today = "saturday"
    if whatistoday == '6':
        today = "sunday"
    return today

def whattriggerday():
    whichtrig = str(input)
    bot.say(whichtrig + " is the day used in the command")
    if whichtrig.endswith('monday'): 
        whichtrigday = 'monday'
    elif whichtrig.endswith('tuesday'): 
        whichtrigday = 'tuesday'
    elif whichtrig.endswith('wednesday'): 
        whichtrigday = 'wednesday'
    elif whichtrig.endswith('thursday'): 
        whichtrigday = 'thursday'
    elif whichtrig.endswith('friday'): 
        whichtrigday = 'friday'
    elif whichtrig.endswith('saturday'): 
        whichtrigday = 'saturday'
    elif whichtrig.endswith('sunday'): 
        whichtrigday = 'sunday'    
    else:
        whichtrigday = 'null'
    return whichtrigday

def whattriggermood():
    whichtrig = str(input)
    bot.say(whichtrig + " is the mood")
    if whichtrig.startswith('.fuck'):
        whichtrigmood = 'salty'
    else:
       whichtrigmood = 'null'
    return whichtrigmood
