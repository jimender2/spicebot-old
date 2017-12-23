#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import datetime
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('today')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    whatistoday, whatdayofweek = whatdayofweeknow()
    daystilfriday = howlonguntilfriday(whatistoday)
    if whatdayofweek == 'Monday':
        specialmsg = "Mondays Suck!"
    if whatdayofweek == 'Tuesday':
        specialmsg = ''
    if whatdayofweek == 'Wednesday':
        specialmsg = "Today is Wednesday, AKA HUMPDAY!!!!"
    if whatdayofweek == 'Thursday':
        specialmsg = ""
    if whatdayofweek == 'Friday':
        specialmsg = ""
    if whatdayofweek == 'Saturday':
        specialmsg = ""
    if whatdayofweek == 'Sunday':
        specialmsg = ""
    botmotd = str("Today is " + str(whatdayofweek) + ". " + str(daystilfriday) + " " + str(specialmsg))
    bot.say(botmotd)
    
def howlonguntilfriday(whatistoday):
    fridaynumber = '4'
    if whatistoday == fridaynumber:
        daystilfriday = "TGIF! It's finally here!!!"
    elif whatistoday == '5' or whatistoday == '6':
        daystilfriday = "It's the Weekend!"
    else:
        daysmath = int(fridaynumber) - int(whatistoday)
        if daysmath == int('1'):
            daystilfriday = "Unfortunately Friday is " + str(daysmath) + " day away. I'm sure we'll make it there!"
        else:
            daystilfriday = "Unfortunately Friday is " + str(daysmath) + " days away. I'm sure we'll make it there!"
    return daystilfriday
    
def whatdayofweeknow():
    whatistoday = str(datetime.datetime.today().weekday())
    if whatistoday == '0':
        whatdayofweek = "Monday"
    elif whatistoday == '1':
        whatdayofweek = "Tuesday"
    elif whatistoday == '2':
        whatdayofweek = "Wednesday"
    elif whatistoday == '3':
        whatdayofweek = "Thursday"
    elif whatistoday == '4':
        whatdayofweek = "Friday"
    elif whatistoday == '5':
        whatdayofweek = "Saturday"
    elif whatistoday == '6':
        whatdayofweek = "Sunday"
    return whatistoday, whatdayofweek
