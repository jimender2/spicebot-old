import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('yourcommandhere')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if not trigger.group(2):
        bot.say('response')

## React to /me (ACTION) challenges
#@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
#@module.intent('ACTION')

##############
## Triggers ##
##############

# .argtest Word1 Word2 Word3 Word4 Word5 Word6 Word7 Word8 Word9
# trigger.args[1] = .argtest Word1 Word2 Word3 Word4 Word5 Word6 Word7 Word8 Word9
# trigger.group(0) = .argtest Word1 Word2 Word3 Word4 Word5 Word6 Word7 Word8 Word9
# trigger.group(1) = argtest
# trigger.group(2) = Word1 Word2 Word3 Word4 Word5 Word6 Word7 Word8 Word9
# trigger.group(3) = Word1
# trigger.group(4) = Word2
# trigger.group(5) = Word3
# trigger.group(6) = Word4
# str(trigger.group(2).split(six, 1)[1]).strip() = Word5 Word6 Word7 Word8 Word9
       
# trigger.nick = the person asking command
# trigger.sender = the current room 
# trigger.admin = detects if trigger.nick is a bot admin

##############
## Bot uses ##
##############

# bot.nick = BotNickName
# bot.say('response') = simple reply
# bot.action('response') = the same as a /me action
# bot.notice('response', instigator) = send a privmsg to a user directly

# * if a value is a number it is best to put str(value)

# * sometimes you can only have so many combinations of variables and strings in a bot.say()
# avoind this by doing
# message = str(long + string + is + too + long + for + botsay)
# bot.say(message)

##################
## Funner Usage ##
##################

# This will give you the channel name (assuming the bot only runs in one channel)
#for c in bot.channels:
#    channel = c

# determine if somebody is in the room right now
# if target.lower() not in bot.privileges[channel.lower()]:

# I use this to see if I'm using the dev bot, and overide timeouts
# if bot.nick.endswith('dev'):

# use this to affect all users in the room
#for u in bot.channels[channel].users:
#    target = u
#    # Do something to target

# use this to determine if in privmsg or not
# inchannel = trigger.sender
#if not inchannel.startswith("#"):

# Multi-line replies
#chunks = longtextyouarespliiting.split()
#per_line = 15
#for i in range(0, len(chunks), per_line):
#    currentline = " ".join(chunks[i:i + per_line])
#    bot.say(str(currentline))



##################################
## My Custom Database functions ##
##################################

# * change "challenges"

# Get a value
def get_database_value(bot, nick, databasekey):
    databasecolumn = str('challenges_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

# Set a value
def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('challenges_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)
    
# get current value and update it adding newvalue
def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey)
    databasecolumn = str('challenges_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))

# opttime = get_database_value(bot, instigator, 'opttime')
# set_database_value(bot, instigator, 'opttime', now)
# adjust_database_value(bot, instigator, loot, '1')

# If your get_function is special and does something with the value, use this
#scriptdef = str('get_' + x + '(bot,target)')
#gethowmany = eval(scriptdef)

###################
## Not Bot stuff ##
###################

## Random Item from array
#missions  = ["Protect Technical Angel","INSTALL MOAR PATCHES"]
#mission = random.randint(0,len(missions) - 1)
#mission = str(missions [mission])
# bot.say(mission)

## append and remove from an array
# weaponslist.append(weaponchange)
# weaponslist.remove(weaponchange)
