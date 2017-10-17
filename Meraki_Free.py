import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('meraki','freemeraki')
def meraki(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if trigger.group(2):
            if trigger.group(2) == 'mx':
                bot.say('MX     https://meraki.cisco.com/tc/freemx')
            elif trigger.group(2) == 'switch':
                bot.say('Switch     https://meraki.cisco.com/tc/freeswitch')
            elif trigger.group(2) == 'ap':
                bot.say('AP     https://meraki.cisco.com/tc/freeap')
            else:
                normalrun='true'
        else:
            normalrun='true'
        try:
            if normalrun:
                bot.say('Please specify which product. Choices are MX , AP , or switch .')
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
