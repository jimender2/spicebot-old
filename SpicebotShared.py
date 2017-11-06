## Shared Functions
import sopel.module
from sopel import module, tools
from sopel.module import ADMIN
from sopel.module import event, rule
import time
import os
import sys
import fnmatch
from os.path import exists

JOINTIMEOUT = 60
LASTTIMEOUT = 60
TOOMANYTIMES = 10

## This runs for every custom module and decides if the module runs or not
def spicebot_prerun(bot,trigger):
    
    ## Get Name Of Channel
    botchannel = bot_channelname(bot, trigger)
    
    ## Nick of user operating command
    instigator = trigger_instigator(bot, trigger)
    
    ## User's Bot Status
    instigatorbotstatus = get_disenable(bot, instigator)
    
    ## Enable Status default is 1 = don't run
    enablestatus = 1
    
    ## Get User's current total uses
    usertotal = get_usertotal(bot, instigator)
    
    ## When Did the user Join The room
    jointime = get_jointime(bot, instigator)
    
    ## When Did the User Last Use the bot
    lasttime = get_lasttime(bot, instigator)
    
    ## Has The user already been warned?
    warned = get_userwarned(bot, instigator)
    
    ## Check user has spicebotenabled
    if not instigatorbotstatus and not warned:
        message = str(instigator + ", you have to run .spicebot on to allow her to listen to you.")
    elif not instigatorbotstatus and warned:
        message = str(instigator + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.")
    
    ## Make sure the user hasn't overdone the bot in the past hour
    elif instigatorbotstatus and usertotal > TOOMANYTIMES and botchannel.startswith("#") and not bot.nick.endswith('dev'):
        message = str(instigator + ", you must have used Spicebot more than 10 times this past hour.")
    
    ## Make sure the user hasn't just entered the room
    elif instigatorbotstatus and jointime < JOINTIMEOUT and botchannel.startswith("#") and not bot.nick.endswith('dev'):
        jointimemath = int(JOINTIMEOUT - jointime)
        message = str(instigator + ", you need to wait " + str(jointimemath) + " seconds to use Spicebot.")
    
    ## Make users wait between uses
    elif instigatorbotstatus and lasttime < LASTTIMEOUT and botchannel.startswith("#") and not bot.nick.endswith('dev'):
        lasttimemath = int(LASTTIMEOUT - lasttime)
        message = str(instigator + ", you need to wait " + str(lasttimemath) + " seconds to use Spicebot.")
    
    ## if user passes ALL above checks, we'll run the module
    else:
        enablestatus = 0
        message = ''
    
        ## Update user total
        if botchannel.startswith("#"):
            update_usernicktotal(bot, instigator)
    
    ## Update user's last use timestamp
    if botchannel.startswith("#") and not bot.nick.endswith('dev'):
        update_usernicktime(bot, instigator)
    
    ## message, if any
    bot.notice(message, instigator)
    
    ## Send Status Forward
    return enablestatus

## Auto Mod
## Auto Mod
@event('JOIN','PART','QUIT','NICK')
@rule('.*')
def greeting(bot, trigger):
    target = trigger.nick
    set_jointime(bot, target)

@sopel.module.interval(3600)
def autoblockhour(bot):
    for channel in bot.channels:
        now = time.time()
        bot.db.set_nick_value(channel, 'spicebothourstart_time', now)
        for u in bot.privileges[channel.lower()]:
            target = u
            bot.db.set_nick_value(target, 'spicebot_usertotal', '')
            bot.db.set_nick_value(target, 'spicebothour_warn', '')

@sopel.module.interval(60)
def autoblock(bot):
    for channel in bot.channels:
        for u in bot.privileges[channel.lower()]:
            target = u
            usertotal = get_usertotal(bot, target)
            if usertotal > TOOMANYTIMES and not bot.nick.endswith('dev'):
                set_timeout(bot, target)
                set_disable(bot, target)
                warn = get_warned(bot, target)
                if not warn:
                    bot.notice(target + ", your access to spicebot has been disabled for an hour. If you want to test her, use ##SpiceBotTest", target)
                    bot.db.set_nick_value(target, 'spicebothour_warn', 'true')

#####################################################################################################################################
## Below This Line are Shared Functions
#####################################################################################################################################

## Name of channel
def bot_channelname(bot, trigger):
    botchannel = trigger.sender
    return botchannel

## Instigator
def trigger_instigator(bot, trigger):
    instigator = trigger.nick
    return instigator

## Users Bot Status
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable

def set_disable(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebot_disenable', '')
    
## User Total
def get_usertotal(bot, instigator):
    usertotal = bot.db.get_nick_value(instigator, 'spicebot_usertotal') or 0
    return usertotal

def reset_count(bot, nick):
    bot.db.set_nick_value(nick, 'spicebot_usertotal', '')
    
## Join Time
def get_jointime(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebotjoin_time') or 0
    return abs(now - last)

def set_jointime(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebotjoin_time', now)
    
## Last Usage
def get_lasttime(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebotlast_time') or 0
    return abs(now - last)

## User warned or not
def get_userwarned(bot, instigator):
    warned = bot.db.get_nick_value(instigator, 'spicebothour_warn') or 0
    return warned

def reset_warn(bot, nick):
    bot.db.set_nick_value(nick, 'spicebothour_warn', '')
    
## Update user total
def update_usernicktotal(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)

## Update user's last use timestamp
def update_usernicktime(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebotlast_time', now)

## timeout
def get_timeout(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebotopt_time') or 0
    return abs(now - last)

def set_timeout(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebotopt_time', now)
    
def reset_timeout(bot, nick):
    bot.db.set_nick_value(nick, 'spicebotopt_time', '')
    
## hour reset
def get_spicebothourstart(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebothourstart_time') or 0
    return abs(now - last)
