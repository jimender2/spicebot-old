from sopel import module

def monday(bot, input):
    whichtrig = str(monday.commands)
    bot.say('monday')
    bot.say(whichtrig)
monday.commands = ['monday','fuckmondays']

def tuesday(bot, input):
    bot.say('tuesday')
tuesday.commands = ['tuesday']

def wednesday(bot, input):
    bot.say('wednesday')
wednesday.commands = ['wednesday']

def thursday(bot, input):
    bot.say('thursday')
thursday.commands = ['thursday']

def friday(bot, input):
    bot.say('friday')
friday.commands = ['friday']

def saturday(bot, input):
    bot.say('saturday')
saturday.commands = ['saturday']

def sunday(bot, input):
    bot.say('sunday')
sunday.commands = ['sunday']
