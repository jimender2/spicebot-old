import sopel.module
from sopel import module, tools
from sopel.module import ADMIN
from sopel.module import event, rule
import time
import os
import sys
import fnmatch
from os.path import exists
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

OPTTIMEOUT = 1800
FINGERTIMEOUT = 1800
TOOMANYTIMES = 10
LASTTIMEOUT = 60

@sopel.module.commands('spicebot')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    instigator = trigger.nick
    inchannel = trigger.sender
    for c in bot.channels:
        channel = c
    options = str("options, warn, channel, modulecount, owner, github, timeout, usage")
    if not trigger.group(2):
        bot.say("That's my name. Don't wear it out!")
    else:
        commandused = trigger.group(2)
        if commandused == 'options':
            bot.say(str(options))
        if commandused == 'warn':
            bot.msg(channel, "This is just a warning. Overuse of the bot, can get you kicked or banned by an operator. If you want to purely play with the bot, go to ##SpiceBotTest, or send Spicebot a PrivateMessage.")
        elif commandused == 'channel':
            bot.say("You can find me in " + channel)
        elif commandused == 'modulecount':
            modulecount = str(len(fnmatch.filter(os.listdir(moduledir), '*.py')))
            bot.say('There are currently ' + modulecount +' custom modules installed.')
        elif commandused == 'owner':
            bot.say(bot.config.core.owner)
        elif commandused == 'github':
            bot.say('Spiceworks IRC Modules     https://github.com/deathbybandaid/sopel-modules')
        elif commandused.startswith('timeout') and not inchannel.startswith("#"):
            target = commandused.replace('timeout','').strip()
            if target == '':
                target = trigger.nick
            bot.say(str(target))
            if not target == trigger.nick and trigger.admin:
                lasttime = get_lasttime(bot, target)
                if lasttime < LASTTIMEOUT:
                    lasttimemath = int(LASTTIMEOUT - lasttime)
                    message = str(target + " needs to wait " + str(lasttimemath) + " seconds to use Spicebot.")
                else:
                    message = str(target + " should be able to use SpiceBot")
            else:
                message = str(target + ", you can't check other's timeouts.")
            bot.notice(message, instigator)
        
            

## Functions

def get_jointime(bot, nick):
    jointime = bot.db.get_nick_value(nick, 'spicebotjoin_time') or 0
    return jointime

def set_jointime(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebotjoin_time', now)
    
def get_timeout(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebotopt_time') or 0
    return abs(now - last)

def set_timeout(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebotopt_time', now)
    
def reset_timeout(bot, nick):
    bot.db.set_nick_value(nick, 'spicebotopt_time', '')

def reset_warn(bot, nick):
    bot.db.set_nick_value(nick, 'spicebothour_warn', '')
    
def reset_count(bot, nick):
    bot.db.set_nick_value(nick, 'spicebot_usertotal', '')
    
def set_disable(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'spicebot_disenable', '')
    
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable

def get_warned(bot, nick):
    warned = bot.db.get_nick_value(nick, 'spicebothour_warn') or 0
    return warned

def get_usertotal(bot, target):
    usertotal = bot.db.get_nick_value(target, 'spicebot_usertotal') or 0
    return usertotal

def get_spicebothourstart(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebothourstart_time') or 0
    return abs(now - last)

def get_lasttime(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'spicebotlast_time') or 0
    return abs(now - last)
