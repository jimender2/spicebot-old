import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('meraki','freemeraki')
def meraki(bot, trigger):
    target = trigger.nick
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

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
