import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('devescuse','devesxuse')
def learntospell(bot, trigger):
    bot.say('You typed .' + trigger.group(1) + ' , You may need to learn to spell.')
