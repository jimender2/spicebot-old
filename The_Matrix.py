import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('matrix') 
def matrix(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if trigger.group(2):
            if trigger.group(2) == 'redpill':
                bot.say('You take the red pill, you stay in Wonderland, and I show you how deep the rabbit hole goes.')
            elif trigger.group(2) == 'bluepill':
                bot.say('You take the blue pill, the story ends. You wake up in your bed and believe whatever you want to believe.')
            else:
                normalrun='true'
        else:
            normalrun='true'
        try:
            if normalrun:
                bot.say('You have two choices. redpill Or bluepill')        
        except UnboundLocalError:
            return
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
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
