import sopel.module
from sopel import module, tools
import time

OPTTIMEOUT = 3600
TOOMANYTIMES = 10

@module.require_chanmsg
@sopel.module.commands('spiceboton','spicebotoff')
def isshelistening(bot,trigger):
    instigator = trigger.nick
    channel = trigger.sender
    target = trigger.group(3) or trigger.nick
    commandtrimmed = trigger.group(1)
    commandtrimmed = str(commandtrimmed.split("spicebot", 1)[1])
    if not trigger.admin and target != trigger.nick:
        bot.say("Only bot admins can mark other users ability to use " + bot.nick + ".")
    elif target == 'all' and commandtrimmed == 'off':
        bot.say('Disabling ' + bot.nick + ' for all.')
        for u in bot.channels[channel].users:
            target = u
            disenable = get_disenable(bot, target)
            if disenable:
                bot.db.set_nick_value(target, 'spicebot_disenable', '')
        bot.say(bot.nick + ' disabled for all.')
    elif target.lower() not in bot.privileges[channel.lower()]:
        bot.say("I'm not sure who that is.")     
    else:
        disenable = get_disenable(bot, target)
        opttime = get_timeout(bot, target)
        if opttime < OPTTIMEOUT and not bot.nick.endswith('dev'):
            bot.notice(target + " can't enable/disable bot listening for %d seconds." % (OPTTIMEOUT - opt_time), instigator)
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

def get_timeout(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebotopt_time') or 0
    return abs(now - last)

def set_timeout(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebotopt_time', now)

def set_disable(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebot_disenable', '')
    
## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable

@sopel.module.interval(60)
def autoblock(bot):
    for channel in bot.channels:
        fingertime = bot.db.get_nick_value(channel, 'spicebothour_time') or 0
        if fingertime >= 60:# and not bot.nick.endswith('dev'):
            for u in bot.privileges[channel.lower()]:
                target = u
                bot.db.set_nick_value(target, 'spicebot_usertotal', '')
                bot.db.set_nick_value(target, 'spicebothour_warn', '')
            bot.db.set_nick_value(channel, 'spicebothour_time', '')
        elif fingertime < 60:# and not bot.nick.endswith('dev'):
            for u in bot.privileges[channel.lower()]:
                target = u
                usertotal = bot.db.get_nick_value(target, 'spicebot_usertotal') or 0
                if usertotal > TOOMANYTIMES:
                    set_timeout(bot, target)
                    set_disable(bot, target)
                    warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
                    if not warned:
                        bot.msg(channel, 'warned is null for' + str(target))
                        bot.db.set_nick_value(target, 'spicebothour_warn', 'true')
                        bot.notice(target + ", your access to spicebot has been disabled for an hour. If you want to test her, use ##SpiceBotTest", target)
        bot.db.set_nick_value(channel, 'spicebothour_time', fingertime + 1)

@module.require_chanmsg
@sopel.module.commands('spicebotcountzero')
def discount(bot,trigger):
    target = trigger.nick
    bot.db.set_nick_value(target, 'spicebot_usertotal', '')
    
@module.require_chanmsg
@sopel.module.commands('spicebotwarned')
def discounter(bot,trigger):
    target = trigger.nick
    warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
    bot.say(str(target) + str(warned))
    
@module.require_chanmsg
@sopel.module.commands('spicebothourzero')
def discounted(bot,trigger):
    for channel in bot.channels:
        bot.db.set_nick_value(channel, 'spicebothour_time', '')

@module.require_chanmsg
@sopel.module.commands('spicebotforcewarn')
def discounteder(bot,trigger):
    bot.db.set_nick_value(target, 'spicebothour_warn', 'true')
