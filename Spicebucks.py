import sopel.module
import datetime
from sopel import module, tools
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

## All commands will use .spicebucks [action]
## Actions to include
### payday - Recieve a once a day payday amount (current Thought is 5 / day)
### bank - Check amount in bank
### transfer - Transfer money from one user to another

#db, channel= current channel, 

@sopel.module.commands('spicebucks')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    for c in bot.channels:
        channel = c
    commandused = trigger.group(3)
    inchannel = trigger.sender
    if commandused:
        if commandused.startswith('payday'):
            checkpayday(bot,trigger.nick)
        elif commandused.startswith('bank'):
            bot.say(checkbank(bot, trigger.nick))
        elif commandused.startswith('transfer'):
            bot.say('transfer money to another user')
            
##### Lots to do

def checkpayday(bot, target):
    now = datetime.datetime.now()
    datetoday = int(now.strftime("%Y%j"))
    bot.say(datetoday)

def spicebuckstransaction(instigator, target, plusminus, amount):
    ### use this to add or remove spicebucks from a user.  Returns True if successful
    ### keep do not use this for spicebot.say or notify.  Use the calling function to do that so that you can say whatever you want.
    #def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('challenges_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)
    
def checkbank(bot, nick):
    points = bot.db.get_nick_value(nick, 'spicebucks_spicebucks') or 1
    return points


