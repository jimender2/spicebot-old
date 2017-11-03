import sopel.module
from sopel import module, tools
from sopel.module import ADMIN
from sopel.module import event, rule
import time

OPTTIMEOUT = 3600
FINGERTIMEOUT = 3600
TOOMANYTIMES = 10
LASTTIMEOUT = 120

@sopel.module.commands('spiceboton','spicebotoff','spicebottimereset')
def isshelistening(bot,trigger):
    for c in bot.channels:
        room = c
    instigator = trigger.nick
    channel = trigger.sender
    target = trigger.group(3) or trigger.nick
    commandtrimmed = trigger.group(1)
    commandtrimmed = str(commandtrimmed.split("spicebot", 1)[1])
    if not trigger.admin and target != trigger.nick:
        bot.say("Only bot admins can mark other users ability to use " + bot.nick + ".")
    elif target == 'all' and commandtrimmed == 'off':
        bot.say('Disabling ' + bot.nick + ' for all.')
        for u in bot.channels[room].users:
            target = u
            disenable = get_disenable(bot, target)
            if disenable:
                bot.db.set_nick_value(target, 'spicebot_disenable', '')
        bot.say(bot.nick + ' disabled for all.')
    elif target.lower() not in bot.privileges[room.lower()]:
        bot.say("I'm not sure who that is.")     
    else:
        disenable = get_disenable(bot, target)
        opttime = get_timeout(bot, target)
        if opttime < OPTTIMEOUT and not bot.nick.endswith('dev') and not trigger.admin:
            bot.notice(target + " can't enable/disable bot listening for %d seconds." % (OPTTIMEOUT - opttime), instigator)
        elif commandtrimmed == 'on':
            if not disenable:
                bot.db.set_nick_value(target, 'spicebot_disenable', 'true')
                bot.say(bot.nick + ' has been enabled for ' + target)
                set_timeout(bot, target)
            else:
                bot.say(bot.nick + ' is already enabled for ' + target)
        elif commandtrimmed == 'off':
            if not disenable:
                bot.say(bot.nick + ' is already disabled for ' + target)
            else:
                bot.db.set_nick_value(target, 'spicebot_disenable', '')
                bot.say(bot.nick + ' has been disabled for ' + target)
                set_timeout(bot, target)
        elif commandtrimmed == 'timereset' and trigger.admin:
            reset_timeout(bot, target)
            
@event('JOIN','PART','QUIT','NICK')
@rule('.*')
def greeting(bot, trigger):
    target = trigger.nick
    jointime = get_jointime(bot, target)
    if not jointime:
        set_jointime(bot, target)

@sopel.module.interval(3600)
def autoblockhour(bot):
    for channel in bot.channels:
        now = time.time()
        bot.msg(channel, 'setting hour start for ' + str(channel) + ' for ' + str(now))
        bot.db.set_nick_value(channel, 'spicebothourstart_time', now)
        for u in bot.privileges[channel.lower()]:
            target = u
            bot.msg(channel, 'cleaning total for' + str(target))
            bot.db.set_nick_value(target, 'spicebot_usertotal', '')
            bot.db.set_nick_value(target, 'spicebothour_warn', '')

@sopel.module.interval(60)
def autoblock(bot):
    for channel in bot.channels:
        bot.msg(channel, 'scanning ' + str(channel) + ' for autoblock')
        for u in bot.privileges[channel.lower()]:
            target = u
            usertotal = get_usertotal(bot, target)
            bot.msg(channel, str(target) + ' has ' + str(usertotal) + ' uses')
            if int(usertotal) > int(TOOMANYTIMES):
                bot.msg(channel, str(target) + ' has exceeded max uses this hour')
                set_timeout(bot, target)
                set_disable(bot, target)
                warn = get_warned(bot, target)
                if not warn:
                    bot.notice(target + ", your access to spicebot has been disabled for an hour. If you want to test her, use ##SpiceBotTest", target)
                    bot.db.set_nick_value(target, 'spicebothour_warn', 'true')
                    
def get_jointime(bot, nick):
    jointime = bot.db.get_nick_value(nick, 'spicebotjoin_time') or 0
    return jointime

def set_jointime(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebotjoin_time', now)
    
def get_timeout(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebotopt_time') or 0
    return abs(now - last)

def set_timeout(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebotopt_time', now)
    
def reset_timeout(bot, nick):
    bot.db.set_nick_value(nick, 'spicebotopt_time', '')

def set_disable(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebot_disenable', '')
    
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable

def get_warned(bot, nick):
    warned = bot.db.get_nick_value(nick, 'spicebothour_warn') or 0
    return warned

def get_usertotal(bot, target):
    usertotal = bot.db.get_nick_value(target, 'spicebot_usertotal') or 0
    return usertotal



def get_spicebothourstart(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebothourstart_time') or 0
    return abs(now - last)



@sopel.module.commands('spicebottotalusesthishour')
def isshelisteningtome(bot,trigger):
    inchannel = trigger.sender
    if not inchannel.startswith("#"):
        target = trigger.group(3) or trigger.nick
        usertotal = get_usertotal(bot, target)
        bot.say(str(usertotal))

@sopel.module.commands('spicebottimeleft')
def canshelistening(bot,trigger):
    inchannel = trigger.sender
    instigator = trigger.nick
    target = trigger.nick
    lasttime = get_lasttime(bot, target)
    if not inchannel.startswith("#"):
        if lasttime < LASTTIMEOUT:
            lasttimemath = int(LASTTIMEOUT - lasttime)
            message = str(target + ", you need to wait " + str(lasttimemath) + " seconds to use Spicebot.")
        else:
            message = str(target + ", you should be able to use SpiceBot")
        bot.notice(message, instigator)
    
def get_lasttime(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebotlast_time') or 0
    return abs(now - last)
    
