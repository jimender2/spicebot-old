ding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('vote','rate','poll')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'vote')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    commandused = trigger.group(1)
    choice = get_trigger_args(triggerargsarray,1)
    yesvotes=0
    novotes = 0
    ratings = []
    pollchoice = []
    if commandused == 'vote':      
        if choice == 'yes' or choice == 'ya':
            yesvotes+=1
        elif choice == 'no' or choice == 'na':
            novotes+=1
        elif choice=='results':
            bot.say(str(yesvotes) + " votes for yes and " str(novotes) + " no votes")
        else:
            bot.say("Vote yes or no")
    elif commandused == 'rate':
        if not choice:
            bot.say("Rate on scale of 1 through 10")
        elif choice.isdigit()
            if choice < = 10 and choice >=1
                ratings.append(choice)
            else
                bot.say("Please rate on a scale from 1 to 10")
        elif choice=='results':
            bot.say("Average rating is ")
        else:
             bot.say("Please rate on a scale from 1 to 10")            
            
    elif commandused == 'poll':
        bot.say("Enter choice a through d)
