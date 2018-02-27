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
    choice = get_trigger_arg(bot, triggerargsarray,1)
    player=trigger.nick
    if commandused == 'vote': 
        if choice=='results':
           getvotes(bot)
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
                set_botdatabase_value(bot,bot.nick,'voting',1)
                set_botdatabase_value(bot,bot.nick,'votechannel',trigger.sender)
            elif choice == 'no' or choice == 'na':
                bot.notice("Your no vote has been recorded", player)
                adjust_botdatabase_value(bot,bot.nick, 'novotes', 1)
                adjust_botdatabase_array(bot, bot.nick, player, 'voters', 'add')
                set_botdatabase_value(bot,bot.nick,'voting',1)
                set_botdatabase_value(bot,bot.nick,'votechannel',trigger.sender)

            else:
                bot.say("Vote yes or no")
            #else:
                #bot.say("You have already voted")
        
    elif commandused == 'rate':
        raters = get_botdatabase_value(bot, bot.nick, 'raters') or []
        if not choice:
            bot.say("Rate on scale of 0 through 10")
         elif choice=='results':
            getrating(bot)            
        else:
            if isfloat(choice):
                choice=float(choice)
                if choice >10:
                    choice = 10
                bot.notice("Your rating of " + str(choice) + " has been recorded", player)
                adjust_botdatabase_array(bot, bot.nick, player, 'raters', 'add')
                adjust_botdatabase_array(bot, bot.nick, choice, 'ratings', 'add')
                set_botdatabase_value(bot,bot.nick,'voting',2)
                set_botdatabase_value(bot,bot.nick,'votechannel',trigger.sender)                
            else:
                bot.say(str(choice) + "is not a number between 0 and 10")
       
             
            
    elif commandused == 'poll':
        bot.say("WIP")
                
def clearvoting(bot):
    reset_botdatabase_value(bot,bot.nick,'novotes')
    reset_botdatabase_value(bot,bot.nick,'yesvotes')
    reset_botdatabase_value(bot,bot.nick,'voters')
    reset_botdatabase_value(bot,bot.nick,'voting')
    reset_botdatabase_value(bot,bot.nick,'raters')
    reset_botdatabase_value(bot,bot.nick,'ratings')
    reset_botdatabase_value(bot,bot.nick,'votechannel')
   
    
    
@sopel.module.interval(30)
def countdown(bot):
    currentsetting = get_botdatabase_value(bot,bot.nick,'voting')
    if currentsetting == 1:
        getvotes(bot)
    elif currentsetting == 2:
        getrating(bot)
        
def getvotes(bot):
    novotes = get_botdatabase_value(bot, bot.nick, 'novotes') or 0
    yesvotes = get_botdatabase_value(bot, bot.nick, 'yesvotes') or 0
    channel = get_botdatabase_value(bot,bot.nick,'votechannel')
    dispmsg = str(yesvotes) + " votes for yes and " + str(novotes) + " no votes"   
    onscreentext(bot, channel, dispmsg)
    clearvoting(bot)
    
def getrating(bot):
    sum=0
    ratings = get_botdatabase_value(bot, bot.nick, 'ratings')
    channel = get_botdatabase_value(bot,bot.nick,'votechannel')
    if ratings:
        for n in ratings:            
            n=int(n)
            sum = sum + n
        average = sum / len(ratings)
        dispmsg = 'The average is ' + str(average)        
        onscreentext(bot, channel, dispmsg)
        clearvoting(bot)
    else:
        dispmsg = 'No ratings found'
        for channel in bot.channels:
            onscreentext(bot, channel, dispmsg)
            
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    

