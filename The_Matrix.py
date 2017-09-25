import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('matrix') 
def matrix(bot, input):
    bot.say('You have two choices. .redpill Or .bluepill')

@sopel.module.rate(120)
@sopel.module.commands('redpill') 
def redpill(bot, input):
    bot.say('You take the red pill, you stay in Wonderland, and I show you how deep the rabbit hole goes.')

@sopel.module.rate(120)
@sopel.module.commands('bluepill')
def bluepill(bot, input):
    bot.say('You take the blue pill, the story ends. You wake up in your bed and believe whatever you want to believe.')
