#!/usr/bin/env python
# coding=utf-8
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
    choice = get_trigger_arg(triggerargsarray,1)
    player=trigger.nick
    if commandused == 'vote': 
        if choice=='results':
            novotes = get_botdatabase_value(bot, bot.nick, 'novotes') or 0
            yesvotes = get_botdatabase_value(bot, bot.nick, 'yesvotes') or 0            
            bot.say(str(yesvotes) + " votes for yes and " + str(novotes) + " no votes")
            clearvoting(bot)
        else:
            yesvotes=0
            novotes = 0
            ratings = []
            pollchoice = []
            voters = get_botdatabase_value(bot, bot.nick, 'voters') or []
            #if player not in voters:
            if choice == 'yes' or choice == 'ya':
                bot.notice("Your yes vote has been recorded", player)
                adjust_botdatabase_value(bot,bot.nick, 'yesvotes', 1)
                adjust_botdatabase_array(bot, bot.nick, player, 'voters', 'add')
            elif choice == 'no' or choice == 'na':
                bot.notice("Your no vote has been recorded", player)
                adjust_botdatabase_value(bot,bot.nick, 'novotes', 1)
                adjust_botdatabase_array(bot, bot.nick, player, 'voters', 'add')             

            else:
                bot.say("Vote yes or no")
            #else:
                #bot.say("You have already voted")
        
    elif commandused == 'rate':
        if not choice:
            bot.say("Rate on scale of 1 through 10")
        elif choice.isdigit():
            if choice <= 10 and choice >=1:
                ratings.append(choice)
            else:
                bot.say("Please rate on a scale from 1 to 10")
        elif choice=='results':
            bot.say("Average rating is ")
        else:
             bot.say("Please rate on a scale from 1 to 10")            
            
    elif commandused == 'poll':
        bot.say("Enter choice a through d")
                
def clearvoting(bot):
    reset_botdatabase_value(bot,bot.nick,'novotes')
    reset_botdatabase_value(bot,bot.nick,'yesvotes')
    reset_botdatabase_value(bot,bot.nick,'voters')
    
