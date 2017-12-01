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
    args = trigger.args[1]
    zero = trigger.group(0)
    one = trigger.group(1)
    two = trigger.group(2)
    three = trigger.group(3)
    four = trigger.group(4)
    five = trigger.group(5)
    six = trigger.group(6)
    sevenandup = str(trigger.group(2).split(six, 1)[1]).strip()
    wordfive = sevenandup(' ', 1)[0]
    wordsix = sevenandup(wordfive, 1)[0]
    wordseven = sevenandup(wordsix, 1)[0]
    wordeight = sevenandup(wordseven, 1)[0]
    wordnine = sevenandup(wordeight, 1)[0]
    wordten = sevenandup(wordnine, 1)[0]
    bot.say("Full command = " + str(args) + " = trigger.group(args)")
    bot.say("Full command = " + str(zero) + " = trigger.group(0)")
    bot.say("command without period = " + str(one) + " = trigger.group(1)")
    bot.say("words1-? = " + str(two) + " = trigger.group(2)")
    bot.say("word1 = " + str(three) + " = trigger.group(3)")
    bot.say("word2 = " + str(four) + " = trigger.group(4)")
    bot.say("word3 = " + str(five) + " = trigger.group(5)")
    bot.say("word4 = " + str(six) + " = trigger.group(6)")
    bot.say("word5andup = " + str(sevenandup) + " = str(trigger.group(2).split(six, 1)[1]).strip()")
    bot.say("word5 = " + str(wordfive) + " = sevenandup(' ', 1)[0]")
    bot.say("word6 = " + str(wordsix) + " = sevenandup(wordfive, )[0]")
    bot.say("word7 = " + str(wordseven) + " = sevenandup(wordsix, 1)[0]")
    bot.say("word8 = " + str(wordeight) + " = sevenandup(wordseven, 1)[0]")
    bot.say("word9 = " + str(wordnine) + " = sevenandup(wordeight, 1)[0]")
    bot.say("word10 = " + str(wordten) + " = sevenandup(wordnine, 1)[0]")
