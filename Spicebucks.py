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
    
def execute_main(bot, trigger, args):
    for c in bot.channels:
        channel = c
    commandused = trigger.group(3)
    inchannel = trigger.sender
    if len(args) > 0:
       if args[0] == 'payday':
           checkpayday(bot,trigger.nick)
       elif args[0] == 'reset': #to be removed
           reset(bot,trigger.nick)
       elif args[0] == 'bank':
           bank(bot, trigger.nick)
       elif args[0] == 'transfer':
           if len(args) >= 3:
               transfer(bot, channel, trigger.nick, args[1], args[2])
           else:
               bot.say("You must enter who you would like to transfer spicebucks to, as well as an amount.")
            
def reset(bot, target): ##### to be removed, verify payday
    bot.db.set_nick_value(target, 'spicebucks_payday', 0)

def checkpayday(bot, target):
    now = datetime.datetime.now()
    datetoday = int(now.strftime("%Y%j"))
    lastpayday = bot.db.get_nick_value(target, 'spicebucks_payday') or 0
    if lastpayday == 0 or lastpayday < datetoday:
        bot.db.set_nick_value(target, 'spicebucks_payday', datetoday)
        spicebucks(bot, target, 'plus', 5)
        bot.say("You haven't been paid yet today. Here's your 5 Spicebucks.") #change to notify
    elif lastpayday == datetoday:
        bot.say("You've already been paid today. Now go do some work.")
        
def spicebucks(bot, target, plusminus, amount):
    success = 'false'
    if type(amount) == int:
        inbank = bot.db.get_nick_value(target, 'spicebucks_bank') or 0
        if plusminus == 'plus':
            bot.db.set_nick_value(target, 'spicebucks_bank', inbank + amount)
            success = 'true'
        elif plusminus == 'minus':
            if inbank - amount < 0:
                bot.notify("I'm sorry, you do not have enough spicebucks in the bank to complete this transaction.")
                success = 'false'
            else:
                bot.db.set_nick_value(target, 'spicebucks_bank', inbank - amount)
                success = 'true'            
    else:
        bot.notify("The amount you entered does not appear to be a number.  Transaction failed.")
        success = 'false'
    return success

def bank(bot, nick):
    spicebucks = bot.db.get_nick_value(nick, 'spicebucks_bank') or 0
    bot.say("You have " + str(spicebucks) + " spicebucks in the bank.")

def transfer(bot, channel, instigator, target, amount):
    if not type(amount) == int:
        if amount <= 0:
            bot.say("I'm sorry, you must enter a proper amount to give to " + target + ".")
        else:
            if target.lower() not in bot.privileges[channel.lower()]:
                bot.say("I'm sorry, I do not know who you want to transfer money to.")
            else:
                if spicebucks(bot, instigator, 'minus', amount) == 'true':
                    spicebucks(bot, target, 'plus', amount)
                    bot.say("You successfully transfered " + amount + " to " + target + ".")

