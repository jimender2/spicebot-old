from sopel import module

def matrix(bot, input):
    bot.say('You have two choices. .redpill Or .bluepill')
matrix.commands = ['matrix']

def redpill(bot, input):
    bot.say('You take the red pill, you stay in Wonderland, and I show you how deep the rabbit hole goes.')
redpill.commands = ['redpill']

def bluepill(bot, input):
    bot.say('You take the blue pill, the story ends. You wake up in your bed and believe whatever you want to believe.')
bluepill.commands = ['bluepill']
