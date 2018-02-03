from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
from sopel import module, tools
import random
from random import randint
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *
from decimal import *
getcontext().prec = 25
@sopel.module.commands('pi')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    digitcount = get_trigger_arg(triggerargsarray, 1) or ''
    if not digitcount == '':
        if not digitcount.isdigit():
            bot.say("Please enter the number of digits you want to see.")
        else:
            digits=int(digitcount)
            if digits>=1 and digits<=10000:
                mynumber =chudnovskyBig(digits)
                bot.say(str(mynumber))
            else:
                bot.say("Please select a number of decimal places between 1 and 100")
    else:
        numberofplaces = random.randint(1,100)
        mynumber = chudnovskyBig(numberofplaces)
        bot.say(str(mynumber))
            
    
    
def chudnovskyBig(n): #http://en.wikipedia.org/wiki/Chudnovsky_algorithm
    pi = Decimal(0) 
    a= 1
    b= 3
    k = 0
    while k<n
        pi = pi + ((4/a)-(4/b))
        a+=4
        b+=4
        k+=1
    return pi
                

