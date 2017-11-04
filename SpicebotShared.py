## Shared Functions
import sopel.module
import time

JOINTIMEOUT = 60
LASTTIMEOUT = 60
TOOMANYTIMES = 10

## This runs for every custom module and decides if the module runs or not
def spicebot_prerun(bot,trigger):
    inchannel = trigger.sender
    instigator = trigger.nick
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    
    ## Enable Status default is 1 = don't run
    enablestatus = 1
    
    ## Check user has spicebotenabled
    if targetdisenable:
        usertotal = get_usertotal(bot, target)
        jointime = get_jointime(bot, target)
        lasttime = get_lasttime(bot, target)
        
        ## Make sure the user hasn't overdone the bot in the past hour
        if usertotal > TOOMANYTIMES and inchannel.startswith("#"):# and not bot.nick.endswith('dev'):
            message = str(target + ", you must have used Spicebot more than 10 times this past hour.")
        
        ## Make sure the user hasn't just entered the room
        elif jointime < JOINTIMEOUT and inchannel.startswith("#"):# and not bot.nick.endswith('dev'):
            jointimemath = int(JOINTIMEOUT - jointime)
            message = str(target + ", you need to wait " + str(jointimemath) + " seconds to use Spicebot.")
            
        ## Make users wait between uses
        elif lasttime < LASTTIMEOUT and inchannel.startswith("#"):# and not bot.nick.endswith('dev'):
            lasttimemath = int(LASTTIMEOUT - lasttime)
            message = str(target + ", you need to wait " + str(lasttimemath) + " seconds to use Spicebot.")
            
        ## if user passes above checks, we'll run the module
        else:
            enablestatus = 0
            message = ''
            
        ## Update user
        if inchannel.startswith("#"):
            update_usernicktotal(bot, target)
        if inchannel.startswith("#"):# and not bot.nick.endswith('dev'):
            update_usernicktime(bot, target)
        
    ## If spicebot is not enabled, we don't run the module
    else:
        
        ## message depends on if the user was locked out automatically
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            message = str(target + ", you have to run .spiceboton to allow her to listen to you.")
        else:
            message = str(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.")
    
    ## message, if any
    bot.notice(message, instigator)
    
    ## Send Status Forward
    return enablestatus

def update_usernicktotal(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)
    
def update_usernicktime(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebotlast_time', now)
    
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable

def get_lasttime(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebotlast_time') or 0
    return abs(now - last)

def get_jointime(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebotjoin_time') or 0
    return abs(now - last)

def get_usertotal(bot, target):
    usertotal = bot.db.get_nick_value(target, 'spicebot_usertotal') or 0
    return usertotal
