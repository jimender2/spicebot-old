from sopel import module
import datetime

def daybot(bot, input):
    whichtrig = str(input)
    
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
     
    if whichtrig.startswith('.fuck'):
        whichtrigmood = 'salty'
    else:
       whichtrigmood = 'null'
    
    whatistoday = str(datetime.datetime.today().weekday())
    bot.say(whatistoday + " is todays number")
    if whatistoday == '0':
        today = "monday"
    elif whatistoday == '1':
        today = "tuesday"
    elif whatistoday == '2':
        today = "wednesday"
    elif whatistoday == '3':
        today = "thursday"
    elif whatistoday == '4':
        today = "friday"
    elif whatistoday == '5':
        today = "saturday"
    elif whatistoday == '6':
        today = "sunday"
    
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
daybot.commands = ['monday','fuckmonday','tuesday','fucktuesday','wednesday','fuckwednesday','thursday','fuckthursday','friday','fuckfriday','saterday','fucksaturday','sunday','fucksunday']
