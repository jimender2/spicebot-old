## Shared Functions
import sopel.module
from sopel import module, tools
from sopel.module import ADMIN
from sopel.module import event, rule
import time
import os
import sys, re
import fnmatch
import random
from os.path import exists

botdevteam = ['deathbybandaid','DoubleD','Mace_Whatdo','dysonparkes','PM','under_score']

JOINTIMEOUT = 60
LASTTIMEOUT = 60
TOOMANYTIMES = 15
OPTTIMEOUT = 1800
FINGERTIMEOUT = 1800
LASTTIMEOUT = 60
LASTTIMEOUTHOUR = 3600

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
        message = str(instigator + ", you have to run .spicebot on to allow her to listen to you. For help, see the wiki at https://github.com/deathbybandaid/sopel-modules/wiki/Using-the-Bot.")
    elif not instigatorbotstatus and warned:
        message = str(instigator + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.")
    
    ## Make sure the user hasn't overdone the bot in the past hour
    elif instigatorbotstatus and usertotal > TOOMANYTIMES and botchannel.startswith("#") and not bot.nick.endswith('dev'):
        message = str(instigator + ", you must have used Spicebot more than " + str(TOOMANYTIMES) + " times this past hour.")
    
    ## Make sure the user hasn't just entered the room
    elif instigatorbotstatus and jointime <= JOINTIMEOUT and botchannel.startswith("#") and not bot.nick.endswith('dev'):
        jointimemath = int(JOINTIMEOUT - jointime)
        message = str(instigator + ", you need to wait " + str(jointimemath) + " seconds to use Spicebot.")
    
    ## Make users wait between uses
    elif instigatorbotstatus and lasttime <= LASTTIMEOUT and botchannel.startswith("#") and not bot.nick.endswith('dev') and commandused not in allowedcommandsarray:
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
    
    ## Add usage counter for individual/channel module counts
    adjust_botdatabase_value(bot, botchannel, str(commandused + "usage"), 1)
    adjust_botdatabase_value(bot, trigger.nick, str(commandused + "usage"), 1)
    ## add usage counter for total nick command count
    #adjust_botdatabase_value(bot, trigger.nick, str(trigger.nick + "usage"), 1)
    
    ## message, if any
    bot.notice(message, instigator)
    
    ## Send Status Forward
    return enablestatus, triggerargsarray

#####################################################################################################################################
## Data collection
#####################################################################################################################################

## User data collection
@sopel.module.interval(1800)
def halfhourdatacollection(bot):
    for channel in bot.channels:
        adjust_botdatabase_array(bot, channel, channel, 'channels', 'add')
        for u in bot.privileges[channel.lower()]:
            botusers = get_botdatabase_value(bot, channel, 'botusers') or []
            if u != bot.nick:
                adjust_botdatabase_array(bot, channel, u, 'users', 'add')
            ubotstatus = get_botdatabase_value(bot, u, 'disenable')
            if ubotstatus and u not in botusers and u != bot.nick:
                adjust_botdatabase_array(bot, channel, u, 'botusers', 'add')
            
## Auto Mod
@event('JOIN','PART','QUIT','NICK')
@rule('.*')
def greeting(bot, trigger):
    now = time.time()
    target = trigger.nick
    set_botdatabase_value(bot, target, 'jointime', now)
    lasttime = get_timesince(bot, target, 'lastusagetime')
    if not lasttime or lasttime < LASTTIMEOUTHOUR:
        bot.db.set_nick_value(target, 'spicebot_usertotal', None)
        bot.db.set_nick_value(target, 'spicebothour_warn', None)

@sopel.module.interval(3600)
def autoblockhour(bot):
    for channel in bot.channels:
        now = time.time()
        set_botdatabase_value(bot, u, 'hourstart', now)
        for u in bot.privileges[channel.lower()]:
            set_botdatabase_value(bot, u, 'usertotal', None)
            set_botdatabase_value(bot, u, 'hourwarned', None)

@sopel.module.interval(60)
def autoblock(bot):
    now = time.time()
    for channel in bot.channels:
        for u in bot.privileges[channel.lower()]:
            usertotal = get_botdatabase_value(bot, u, 'usertotal')
            if usertotal > TOOMANYTIMES and not bot.nick.endswith('dev'):
                set_botdatabase_value(bot, u, 'lastopttime', now)
                set_botdatabase_value(bot, u, 'disenable', None)
                warned = get_botdatabase_value(bot, u, 'hourwarned')
                if not warned:
                    bot.notice(u + ", your access to spicebot has been disabled for an hour. If you want to test her, use ##SpiceBotTest", target)
                    set_botdatabase_value(bot, u, 'hourwarned', 'true')
                    
#####################################################################################################################################
## Below This Line are Shared Functions
#####################################################################################################################################

##########
## ARGS ##
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
            rangea = int(rangea)
            rangeb = int(rangeb) + 1
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
        if totalarray > 1:
            totalarray = totalarray -2
            triggerarg = str(triggerargsarray[totalarray])
    elif str(number).endswith("!"):
        number = re.sub(r"!", '', str(number))
        for i in range(1,totalarray):
            if int(i) != int(number):
                arg = get_trigger_arg(triggerargsarray, i)
                if triggerarg != '':
                    triggerarg = str(triggerarg + " " + arg)
                else:
                    triggerarg = str(arg)
    elif number == 'random':
        if totalarray > 1:
            randomselected = random.randint(0,len(triggerargsarray) - 1)
            triggerarg = str(triggerargsarray [randomselected])
    elif number == 'list':
        for x in triggerargsarray:
            if triggerarg != '':
                triggerarg  = str(triggerarg  + ", " + x)
            else:
                triggerarg  = str(x)
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

def get_botdatabase_value(bot, nick, databasekey):
    databasecolumn = str('spicebot_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

def set_botdatabase_value(bot, nick, databasekey, value):
    databasecolumn = str('spicebot_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)
    
def adjust_botdatabase_value(bot, nick, databasekey, value):
    oldvalue = get_botdatabase_value(bot, nick, databasekey) or 0
    databasecolumn = str('spicebot_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))
   
def get_botdatabase_array_total(bot, nick, databasekey):
    array = get_botdatabase_value(bot, nick, databasekey) or []
    entriestotal = len(array)
    return entriestotal

def adjust_database_array(bot, nick, entry, databasekey, adjustmentdirection):
    adjustarray = get_botdatabase_value(bot, nick, databasekey) or []
    adjustarraynew = []
    for x in adjustarray:
        adjustarraynew.append(x)
    set_botdatabase_value(bot, nick, databasekey, None)
    adjustarray = []
    if adjustmentdirection == 'add':
        if entry not in adjustarraynew:
            adjustarraynew.append(entry)
    elif adjustmentdirection == 'del':
        if entry in adjustarraynew:
            adjustarraynew.remove(entry)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        set_botdatabase_value(bot, nick, databasekey, None)
    else:
        set_botdatabase_value(bot, nick, databasekey, adjustarray)

############################
## Fix unicode in strings ##
############################

def unicode_string_cleanup(string):
    for r in (("\u2013", "-"), ("\u2019", "'"), ("\u2026", "...")):
        string = string.replace(*r)
    return string
    
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
