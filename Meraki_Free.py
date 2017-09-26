import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('meraki','freemeraki')
def meraki(bot, trigger):
    if trigger.group(2):
        if trigger.group(2) == 'mx':
            bot.say('MX     https://meraki.cisco.com/tc/freemx')
        if trigger.group(2) == 'switch':
            bot.say('Switch     https://meraki.cisco.com/tc/freeswitch')
        if trigger.group(2) == 'ap':
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
