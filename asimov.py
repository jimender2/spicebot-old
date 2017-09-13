import sopel.module

@sopel.module.commands('asimov')
def asimov(bot, trigger):
    bot.say('1.  A robot may not injure a human being or, through inaction, allow a human being to come to harm.')
    bot.say('2.  A robot must obey orders given it by human beings except where such orders would conflict with the First Law.')
    bot.say('3.  A robot must protect its own existence as long as such protection does not conflict with the First or Second Law.')
