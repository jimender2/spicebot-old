import sopel.module

@sopel.module.commands('devescuse')
def learntospell(bot, trigger):
    bot.say('You typed .' + trigger.group(1) + ' , You may need to learn to spell.')
