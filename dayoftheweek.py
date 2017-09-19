from sopel import module
import datetime

def daybot(bot,trigger):
    whichtrig = trigger.group(1)
    
    #check if whichtrig ends with s
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
daybot.commands = ['monday','mondays','fuckmonday','fuckmondays','tuesday','tuesdays','fucktuesday','fucktuesdays','wednesday','wednesdays','fuckwednesday','fuckwednesdays','thursday','thursdays','fuckthursday','fuckthursdays','friday','fridays','fuckfriday','fuckfridays','saterday','saterdays','fucksaturday','fucksaturdays','sunday','sundays','fucksunday','fucksundays']
