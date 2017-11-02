## Shared Functions
import sopel.module
import time

JOINTIMEOUT = 60
LASTTIMEOUT = 60

## Main Check
def spicebot_prerun(bot,trigger):
    instigator = trigger.nick
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        jointime = get_jointime(bot, target)
        lastjointime = get_lasttime(bot, target)
        if jointime < JOINTIMEOUT:
            enablestatus = 1
            bot.notice(target + ", you need to wait a minute after joining the channel to use Spicebot.", instigator)
        elif lasttime < LASTTIMEOUT:
            enablestatus = 1
            bot.notice(target + ", you need to wait a minute after you use Spicebot.", instigator)
        else:
            enablestatus = 0
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)
        enablestatus = 1
    update_usernick(bot, target)
    return enablestatus


def update_usernick(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebotlast_time', now)
    
## Check Status of Opt In
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
