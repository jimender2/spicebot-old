import sopel
from sopel import module, tools
import random

@sopel.module.commands('blame')
@module.require_chanmsg
def webmd(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    channel = trigger.sender
    targetdisenable = get_spicebotdisenable(bot, target)
    if targetdisenable:
        blametargetarray = []
        for u in bot.channels[channel].users:
            target = u
            disenable = get_spicebotdisenable(bot, target)
            if not disenable:
                blametargetarray.append(target)
        try:
            whotoblame =random.choice(blametargetarray)
        except IndexError:
            whotoblame = str(instigator + "'s mom")
        bot.say("It's " + whotoblame + "'s fault.")
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator) 
    
    
def update_usertotal(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)

## Check Status of Opt In
def get_spicebotdisenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
        
            
            
                
