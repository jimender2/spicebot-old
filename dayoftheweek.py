from sopel import module
import datetime

whatistoday = datetime.datetime.today().weekday()

def monday(bot, input):
    whichtrig = str(input)
    if whichtrig == ".fuckmonday":
        if whatistoday == '0':
            bot.say("This is only the first monday of the week!")
        else:
            bot.say("Mondays really do suck!")
    else:
        if whatistoday == '0':
            bot.say("Today is Monday, what about it?")
        else:
            bot.say("Monday, what about it?")
monday.commands = ['monday','fuckmonday']

def tuesday(bot, input):
    whichtrig = str(input)
    if whichtrig == ".fucktuesday":
        bot.say("This is only the second monday of the week!")
    else:
        bot.say("Tuesday, what about it?")
monday.commands = ['tuesday','fucktuesday']

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
