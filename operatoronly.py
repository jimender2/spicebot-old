import sopel.module
from sopel.module import rule, event, commands, example, OP
from sopel.tools.target import User, Channel

@sopel.module.commands('optest')
def optest(bot,trigger):
    if trigger.nick.ops:
        bot.say('you are op')
    elif not trigger.nick.ops:
        bot.say('you are not op')
    else:
        bot.say("this does not work")

@sopel.module.require_admin
@sopel.module.commands('getops')
def getMembers(bot,trigger):
    #users = str(bot.channels[trigger.sender].users)
    #bot.say(users)
    userlist = []
    for u in bot.channels[trigger.sender].ops:
        bot.say(u)
        userlist.append(u)
    #randno = randint(0,len(userlist))
    #randUser = userlist[randno]
    #bot.say('Here is a randomly picked user: ' + randUser)

    
@sopel.module.commands('optestb')
def optestb(bot,trigger):
    for channel in bot.channels:
        bot.say(str(OP))

@sopel.module.commands('optestc')
def optestc(bot,trigger):
    if trigger.group(4):
        bot.say('hello op')
