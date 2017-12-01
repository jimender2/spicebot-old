# -*- coding: utf-8 -*/
from sopel import module
from sopel.tools import events
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.require_admin
@sopel.module.commands('argtest')
def mainfunction(bot, trigger):
    fullcommandused = trigger.group(2)
    arraynumber = 0
    if trigger.group(2):
        triggerargsarray = []
        for x in fullcommandused:
            triggerargsarray.append(x)
        
        for x in triggerargsarray:
            test = triggerargsarray[arraynumber]
            bot.say(str(arraynumber) + " " + str(test))
            arraynumber = arraynumber + 1
            
    else:
        bot.say("No args given")
    
    #args = trigger.args[1]
    #zero = trigger.group(0)
    #one = trigger.group(1)
    #two = trigger.group(2)
    #three = trigger.group(3)
    #four = trigger.group(4)
    #five = trigger.group(5)
    #six = trigger.group(6)
    #sevenandup = str(trigger.group(2).split(six, 1)[1]).strip()
    #wordfive = splitme(sevenandup, 0)
    #wordfive = sevenandup(' ', 1)[0]
    #wordsix = sevenandup(wordfive, 1)[0]
    #wordseven = sevenandup(wordsix, 1)[0]
    #wordeight = sevenandup(wordseven, 1)[0]
    #wordnine = sevenandup(wordeight, 1)[0]
    #wordten = sevenandup(wordnine, 1)[0]
    #bot.say("Full command = " + str(args) + " = trigger.group(args)")
    #bot.say("Full command = " + str(zero) + " = trigger.group(0)")
    #bot.say("command without period = " + str(one) + " = trigger.group(1)")
    #bot.say("words1-? = " + str(two) + " = trigger.group(2)")
    #bot.say("word1 = " + str(three) + " = trigger.group(3)")
    #bot.say("word2 = " + str(four) + " = trigger.group(4)")
    #bot.say("word3 = " + str(five) + " = trigger.group(5)")
    #bot.say("word4 = " + str(six) + " = trigger.group(6)")
    #bot.say("word5andup = " + str(sevenandup) + " = str(trigger.group(2).split(six, 1)[1]).strip()")
    #bot.say("word5 = " + str(wordfive))
    #bot.say("word6 = " + str(wordsix))
    #bot.say("word7 = " + str(wordseven))
    #bot.say("word8 = " + str(wordeight))
    #bot.say("word9 = " + str(wordnine))
    #bot.say("word10 = " + str(wordten))

#def splitme(text, n):
#    return text.split()[n]
