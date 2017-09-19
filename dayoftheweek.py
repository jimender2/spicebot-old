from sopel import module
import datetime

def daybot(bot, input):
    whichtrig = whattriggerused()
    today = whatdayisit()
    if whichtrig.startswith(".fuck"):
        bot.say(today + "s " + "really do suck!")
    else:
        if today == whichtrig:
            bot.say("Today is" + today + ", what about it?")
        else:
            bot.say(today + ", what about it?")
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

def whattriggerused():
    whichtrig = str(input)
    return whichtrig
