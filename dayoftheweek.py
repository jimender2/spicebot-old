from sopel import module
import datetime

def daybot(bot, input):
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
daybot.commands = ['monday','fuckmonday','tuesday','fucktuesday','wednesday','fuckwednesday','thursday','fuckthursday','friday','fuckfriday','saterday','fucksaturday','sunday','fucksunday',]

def whatdayisit():
    whatistoday = str(datetime.datetime.today().weekday())
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
    if whichtrig.endswith('monday'): 
        whichtrigday = 'monday'
    if whichtrig.endswith('tuesday'): 
        whichtrigday = 'tuesday'
    if whichtrig.endswith('wednesday'): 
        whichtrigday = 'wednesday'
    if whichtrig.endswith('thursday'): 
        whichtrigday = 'thursday'
    if whichtrig.endswith('friday'): 
        whichtrigday = 'friday'
    if whichtrig.endswith('saturday'): 
        whichtrigday = 'saturday'
    if whichtrig.endswith('sunday'): 
        whichtrigday = 'sunday'    
    if not whichtrigday:
        whichtrigday = 'null'
    return whichtrigday

def whattriggermood():
    whichtrig = str(input)
    if whichtrig.startswith('.fuck'):
        whichtrigmood = 'salty'
    else:
       whichtrigmood = 'null'
    if not whichtrigmood:
        whichtrigmood = 'null'
    return whichtrigmood
