import sopel.module
import random

@sopel.module.commands('points','pants')
def points(bot, trigger):
    bot.say(trigger.nick + ' awards ' + random + ' to' + '%s')
