## Shared Functions
import sopel.module
from sopel import module, tools
from sopel.module import ADMIN
from sopel.module import event, rule
import time
import os
import sys, re
import fnmatch
from os.path import exists

JOINTIMEOUT = 60
LASTTIMEOUT = 60
TOOMANYTIMES = 15

## This runs for every custom module and decides if the module runs or not
def spicebot_prerun(bot,trigger):
    
    ## Custom args
    triggerargsarray = create_args_array(trigger.group(2))
    
    ## time
    now = time.time()
    
    ## used to circumvent
    commandused = trigger.group(1)
    allowedcommandsarray = ['duel','challenge']
    
    ## Get Name Of Channel
    botchannel = trigger.sender
    
    ## Nick of user operating command
    instigator = trigger.nick
    
    ## User's Bot Status
    instigatorbotstatus = get_botdatabase_value(bot, instigator, 'disenable')
    
    ## Enable Status default is 1 = don't run
    enablestatus = 1
    
    ## Get User's current total uses
    usertotal = get_botdatabase_value(bot, instigator, 'usertotal')
    
    ## When Did the user Join The room
    jointime = get_timesince(bot, instigator, 'jointime')
    
    ## When Did the User Last Use the bot
    lasttime = get_timesince(bot, instigator, 'lastusagetime')
    
    ## Has The user already been warned?
    warned = get_botdatabase_value(bot, instigator, 'hourwarned')
    
    ## Check user has spicebotenabled
    if not instigatorbotstatus and not warned:
        message = str(instigator + ", you have to run .spicebot on to allow her to listen to you.")
    elif not instigatorbotstatus and warned:
        message = str(instigator + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.")
    
    ## Make sure the user hasn't overdone the bot in the past hour
    elif instigatorbotstatus and usertotal > TOOMANYTIMES and botchannel.startswith("#") and not bot.nick.endswith('dev'):
        message = str(instigator + ", you must have used Spicebot more than " + str(TOOMANYTIMES) + " times this past hour.")
    
    ## Make sure the user hasn't just entered the room
    elif instigatorbotstatus and jointime < JOINTIMEOUT and botchannel.startswith("#") and not bot.nick.endswith('dev'):
        jointimemath = int(JOINTIMEOUT - jointime)
        message = str(instigator + ", you need to wait " + str(jointimemath) + " seconds to use Spicebot.")
    
    ## Make users wait between uses
    elif instigatorbotstatus and lasttime < LASTTIMEOUT and botchannel.startswith("#") and not bot.nick.endswith('dev') and commandused not in allowedcommandsarray:
        lasttimemath = int(LASTTIMEOUT - lasttime)
        message = str(instigator + ", you need to wait " + str(lasttimemath) + " seconds to use Spicebot.")
    
    ## if user passes ALL above checks, we'll run the module
    else:
        enablestatus = 0
        message = ''
    
        ## Update user total
        if botchannel.startswith("#") and not trigger.admin:
            adjust_botdatabase_value(bot, instigator, 'usertotal', '1')
    
    ## Update user's last use timestamp
    if botchannel.startswith("#") and not bot.nick.endswith('dev'):
        set_botdatabase_value(bot, instigator, 'lastusagetime', now)
    
    ## message, if any
    bot.notice(message, instigator)
    
    ## Send Status Forward
    return enablestatus, triggerargsarray



#####################################################################################################################################
## Below This Line are Shared Functions
#####################################################################################################################################

##########
## Args ##
##########

def create_args_array(fullstring):
    triggerargsarray = []
    if fullstring:
        for word in fullstring.split():
            triggerargsarray.append(word)
    return triggerargsarray

def get_trigger_arg(triggerargsarray, number):
    totalarray = len(triggerargsarray)
    totalarray = totalarray + 1
    triggerarg = ''
    if "^" in str(number) or number == 0 or str(number).endswith("+") or str(number).endswith("-") or str(number).endswith("<") or str(number).endswith(">"):
        if str(number).endswith("+"):
            rangea = re.sub(r"\+", '', str(number))
            rangea = int(rangea)
            rangeb = totalarray
        elif str(number).endswith("-"):
            rangea = 1
            rangeb = re.sub(r"-", '', str(number))
            rangeb = int(rangeb) + 1
        elif str(number).endswith(">"):
            rangea = re.sub(r">", '', str(number))
            rangea = int(rangea) + 1
            rangeb = totalarray
        elif str(number).endswith("<"):
            rangea = 1
            rangeb = re.sub(r"<", '', str(number))
            rangeb = int(rangeb)
        elif "^" in str(number):
            rangea = number.split("^", 1)[0]
            rangeb = number.split("^", 1)[1]
        elif number == 0:
            rangea = 1
            rangeb = totalarray
        if rangea <= totalarray:
            for i in range(rangea,rangeb):
                arg = get_trigger_arg(triggerargsarray, i)
                if triggerarg != '':
                    triggerarg = str(triggerarg + " " + arg)
                else:
                    triggerarg = str(arg)
    elif number == 'last':
        totalarray = totalarray -2
        triggerarg = str(triggerargsarray[totalarray])
    else:
        number = int(number) - 1
        try:
            triggerarg = triggerargsarray[number]
        except IndexError:
            triggerarg = ''
    return triggerarg

##############
## Database ##
##############

# Get a value
def get_botdatabase_value(bot, nick, databasekey):
    databasecolumn = str('spicebot_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

# Set a value
def set_botdatabase_value(bot, nick, databasekey, value):
    databasecolumn = str('spicebot_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)
    
# get current value and update it adding newvalue
def adjust_botdatabase_value(bot, nick, databasekey, value):
    oldvalue = get_botdatabase_value(bot, nick, databasekey)
    databasecolumn = str('spicebot_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))

##########
## Time ##
##########

def get_timesince(bot, nick, databasekey):
    now = time.time()
    last = get_botdatabase_value(bot, nick, databasekey) or 0
    return abs(now - int(last))

###########
## Tools ##
###########

def diceroll(howmanysides):
    diceroll = randint(0, howmanysides)
    return diceroll
