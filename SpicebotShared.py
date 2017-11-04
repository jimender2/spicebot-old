## Shared Functions
import sopel.module
import time

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
    warned = bot.db.get_nick_value(instigator, 'spicebothour_warn') or 0
    
    ## Check user has spicebotenabled
    if not instigatorbotstatus and not warned:
        message = str(instigator + ", you have to run .spiceboton to allow her to listen to you.")
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
    
    ## if user passes above checks, we'll run the module
    else:
        enablestatus = 0
        message = ''
    
    ## Update user total
    if inchannel.startswith("#"):
        update_usernicktotal(bot, instigator)
    
    ## Update user's last use timestamp
    if inchannel.startswith("#") and not bot.nick.endswith('dev'):
        update_usernicktime(bot, instigator)
    
    ## message, if any
    bot.notice(message, instigator)
    
    ## Send Status Forward
    return enablestatus

#####################################################################################################################################
## Below This Line are Shared Functions
#####################################################################################################################################

## Name of channel
def bot_channelname(bot, trigger):
    inchannel = trigger.sender
    return inchannel

## Instigator
def trigger_instigator(bot, trigger):
    instigator = trigger.sender
    return instigator

## Users Bot Status
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable

## User Total
def get_usertotal(bot, instigator):
    usertotal = bot.db.get_nick_value(instigator, 'spicebot_usertotal') or 0
    return usertotal

## Join Time
def get_jointime(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebotjoin_time') or 0
    return abs(now - last)

## Last Usage
def get_lasttime(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebotlast_time') or 0
    return abs(now - last)

## Update user total
def update_usernicktotal(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)

## Update user's last use timestamp
def update_usernicktime(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebotlast_time', now)
    
