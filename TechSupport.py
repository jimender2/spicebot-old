import sopel.module
import random

@sopel.module.rate(120)
@sopel.module.commands('techsupport')
def techsupport(bot, trigger):
    messages = ["YOU MUST CONSTRUCT ADDITIONAL PYLONS!","Have you tried flinging feces at it?","Have you tried chewing the cable?","Did you try turning it off and on again?","Did you try licking the mouse? Double-lick?","Did your try replacing all the ones with zeros?"]
    answer = random.randint(0,len(messages) - 1)
    bot.say(messages[answer]);
