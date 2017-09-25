import sopel.module
from sopel.module import OP
from sopel.tools.target import User, Channel

@sopel.module.commands('isop')
def isop(bot,trigger):
    if not trigger.group(2):
        nick = trigger.nick
    else:
        nick = trigger.group(2) + " "
    if bot.privileges[trigger.sender][nick] == OP:
        bot.say(nick + ' is an op.')        
    else: 
        bot.say(nick + ' is not an op.')
        #if bot.privileges[trigger.sender][trigger.nick] == OP:
         #   bot.say(trigger.nick + ', you are op.')
        #elif bot.privileges[trigger.sender][trigger.nick] < OP:
         #   bot.say(trigger.nick + ', you are not op.')
    #else:
       # if bot.privileges[trigger.sender][trigger.group(2)] == OP:
        #    bot.say(trigger.group(2) + ' is op.')
        #elif bot.privileges[trigger.sender][trigger.group(2)] < OP:
         #   bot.say(trigger.group(2).strip() + ' is not op.')
