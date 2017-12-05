import sopel.module
import datetime
from sopel import module, tools
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

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
    if len(args) == 0:
        bot.say("Welcome to the #Spiceworks Bank.  Your options are payday and bank. (for now)")
    elif len(args) >= 1:
        if args[0] == 'payday' or args[0] == 'upupdowndownleftrightleftrightbastart':
            checkpayday(bot,trigger.nick, args[0])
        elif args[0] == 'reset': #to be removed
            reset(bot,trigger.nick)
        elif args[0] == 'bank':
            if len(args) > 1:
                if args[1].lower() not in bot.privileges[channel.lower()]:
                    bot.say("I'm sorry, I do not know who " + args[1] + " is.")
                else:
                    bank(bot, args[1], 'other')
            else:
                bank(bot, trigger.nick, 'self')
        elif args[0] == 'transfer':
            if len(args) >= 3:
                transfer(bot, channel, trigger.nick, args[1], args[2])
            else:
                bot.say("You must enter who you would like to transfer spicebucks to, as well as an amount.")
            
def reset(bot, target): ##### to be removed, verify payday
    bot.db.set_nick_value(target, 'spicebucks_payday', 0)

def checkpayday(bot, target, args):
    now = datetime.datetime.now()
    datetoday = int(now.strftime("%Y%j"))
    lastpayday = bot.db.get_nick_value(target, 'spicebucks_payday') or 0
    if lastpayday == 0 or lastpayday < datetoday:
        paydayamount = 5
        if args == 'upupdowndownleftrightleftrightbastart':
            paydayamount = 15
        bot.db.set_nick_value(target, 'spicebucks_payday', datetoday)
        spicebucks(bot, target, 'plus', paydayamount)
        bot.say("You haven't been paid yet today. Here's your " + str(paydayamount) + " spicebucks.") #change to notify
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
                bot.say("I'm sorry, you do not have enough spicebucks in the bank to complete this transaction.")
                success = 'false'
            else:
                bot.db.set_nick_value(target, 'spicebucks_bank', inbank - amount)
                success = 'true'            
    else:
        bot.say("The amount you entered does not appear to be a number.  Transaction failed.")
        success = 'false'
    return success

def bank(bot, nick, target):
    spicebucks = bot.db.get_nick_value(nick, 'spicebucks_bank') or 0
    identifier = "You have "
    if target == 'other':
        identifier = nick + ' has '
    bot.say(identifier + str(spicebucks) + " spicebucks in the bank.")

def transfer(bot, channel, instigator, target, amount):
    success = 0
    try:
        amount = int(amount)
        success = 1
    except:
        bot.say("I'm sorry, the amount you entered does not appear to be a number.")
        success = 0
    
    if success == 1:
        if amount <= 0:
            bot.say("I'm sorry, you must enter a proper amount to give to " + target + ".")
        else:
            if target.lower() not in bot.privileges[channel.lower()]:
                 bot.say("I'm sorry, I do not know who you want to transfer money to.")
            else:
                spicebucks(bot, instigator, 'minus', amount)
                spicebucks(bot, target, 'plus', amount)
                bot.say("You successfully transfered " + str(amount) + " spicebucks to " + target + ".") 
        
