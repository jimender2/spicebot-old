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
    commandused = trigger.group(2)
    if commandused.startswith('on') or commandused.startswith('off'):
        execute_main(bot, trigger)
    else:
        enablestatus = spicebot_prerun(bot, trigger)
        if not enablestatus:
            execute_main(bot, trigger)

def execute_main(bot, trigger):
    instigator = trigger.nick
    inchannel = trigger.sender
    for c in bot.channels:
        channel = c
    options = str("options, warn, channel, modulecount, owner, github, timeout, usage, status, on/off")
    if not trigger.group(2):
        bot.say("That's my name. Don't wear it out!")
    else:
        commandused = trigger.group(2)
        
        ## give options
        if commandused == 'options':
            bot.say(str(options))
            
        ## Warn
        if commandused == 'warn':
            bot.msg(channel, "This is just a warning. Overuse of the bot, can get you kicked or banned by an operator. If you want to purely play with the bot, go to ##SpiceBotTest, or send Spicebot a PrivateMessage.")
        
        ## Channel
        elif commandused == 'channel':
            bot.say("You can find me in " + channel)
        
        ## how many custom modules
        elif commandused == 'modulecount':
            modulecount = str(len(fnmatch.filter(os.listdir(moduledir), '*.py')))
            bot.say('There are currently ' + modulecount +' custom modules installed.')
        
        ## Bot Owner
        elif commandused == 'owner':
            bot.say(bot.config.core.owner)
        
        ## link to github repo
        elif commandused == 'github':
            bot.say('Spiceworks IRC Modules     https://github.com/deathbybandaid/sopel-modules')
        
        ## How long does a user have to wait to use a command
        elif commandused.startswith('timeout') and not inchannel.startswith("#"):
            target = commandused.replace('timeout','').strip()
            if target == '':
                target = trigger.nick
            if target == instigator or trigger.admin:
                lasttime = get_lasttime(bot, target)
                if lasttime < LASTTIMEOUT:
                    lasttimemath = int(LASTTIMEOUT - lasttime)
                    message = str(target + " needs to wait " + str(lasttimemath) + " seconds to use Spicebot.")
                else:
                    message = str(target + " should be able to use SpiceBot")
            else:
                message = str(target + ", you can't check other's timeouts.")
            bot.notice(message, instigator)
        
        ## How many times in the past hour has the user used the bot
        elif commandused.startswith('usage') and not inchannel.startswith("#"):
            target = commandused.replace('usage','').strip()
            if target == '':
                target = trigger.nick
            if target == instigator or trigger.admin:
                usertotal = get_usertotal(bot, target)
                message = str(target + " has used " + str(usertotal) + " commands this hour.")
            else:
                message = str(target + ", you can't check other's usage.")
            bot.notice(message, instigator)
            
        ## Enable/Disable status
        elif commandused.startswith('status') and not inchannel.startswith("#"):
            target = commandused.replace('status','').strip()
            if target == '':
                target = trigger.nick
            disenable = get_disenable(bot, target)
            if disenable:
                message = str(target + " has SpiceBot enabled")
            else:
                message = str(target + " does not have SpiceBot enabled")
            bot.notice(message, instigator)
        
        ## On/Off
        elif commandused.startswith('on') or commandused.startswith('off'):
            if commandused.startswith('on'):
                target = commandused.replace('on','').strip()
                statuschange = 'enabl'
            else:
                target = commandused.replace('off','').strip()
                statuschange = 'disabl'
            if target == '':
                target = trigger.nick
            if target == 'all':
                if trigger.admin:
                    bot.say(statuschange + 'ing ' + bot.nick + ' for all.')
                    for u in bot.channels[channel].users:
                        target = u
                        disenable = get_disenable(bot, target)
                        if statuschange == 'enabl':
                            bot.db.set_nick_value(target, 'spicebot_disenable', 'true')
                        else:
                            bot.db.set_nick_value(target, 'spicebot_disenable', '')
                    bot.say(bot.nick + ' ' + statuschange + 'ed for all.')
                else:
                    bot.say('Only Admin can Change Statuses for all.')
            elif target.lower() not in bot.privileges[channel.lower()]:
                bot.say("I'm not sure who that is.")
            elif not trigger.admin and target != trigger.nick:
                bot.say("Only bot admins can mark other users ability to use " + bot.nick + ".")
            else:
                disenable = get_disenable(bot, target)
                opttime = get_timeout(bot, target)
                if opttime < OPTTIMEOUT and not bot.nick.endswith('dev') and not trigger.admin:
                    bot.notice(target + " can't enable/disable bot listening for %d seconds." % (OPTTIMEOUT - opttime), instigator)
                elif commandused.startswith('on'):
                    if not disenable:
                        bot.db.set_nick_value(target, 'spicebot_disenable', 'true')
                        bot.say(bot.nick + ' has been enabled for ' + target)
                        set_timeout(bot, target)
                    else:
                        bot.say(bot.nick + ' is already enabled for ' + target)
                elif commandused.startswith('off'):
                    if not disenable:
                        bot.say(bot.nick + ' is already disabled for ' + target)
                    else:
                        bot.db.set_nick_value(target, 'spicebot_disenable', '')
                        bot.say(bot.nick + ' has been disabled for ' + target)
                        set_timeout(bot, target)
                
        ## Resets
        elif commandused == 'timereset' and trigger.admin:
            target = commandused.replace('timereset','').strip()
            if target == '':
                target = trigger.nick
            reset_timeout(bot, target)
        elif commandused == 'warnreset' and trigger.admin:
            target = commandused.replace('warnreset','').strip()
            if target == '':
                target = trigger.nick
            reset_warn(bot, target)
        elif commandused == 'countreset' and trigger.admin:
            target = commandused.replace('countreset','').strip()
            if target == '':
                target = trigger.nick
            reset_count(bot, target)

## Auto Mod

@event('JOIN','PART','QUIT','NICK')
@rule('.*')
def greeting(bot, trigger):
    target = trigger.nick
    jointime = get_jointime(bot, target)
    if not jointime:
        set_jointime(bot, target)

@sopel.module.interval(3600)
def autoblockhour(bot):
    for channel in bot.channels:
        now = time.time()
        bot.db.set_nick_value(channel, 'spicebothourstart_time', now)
        for u in bot.privileges[channel.lower()]:
            target = u
            bot.db.set_nick_value(target, 'spicebot_usertotal', '')
            bot.db.set_nick_value(target, 'spicebothour_warn', '')

@sopel.module.interval(60)
def autoblock(bot):
    for channel in bot.channels:
        for u in bot.privileges[channel.lower()]:
            target = u
            usertotal = get_usertotal(bot, target)
            if usertotal > TOOMANYTIMES and not bot.nick.endswith('dev'):
                set_timeout(bot, target)
                set_disable(bot, target)
                warn = get_warned(bot, target)
                if not warn:
                    bot.notice(target + ", your access to spicebot has been disabled for an hour. If you want to test her, use ##SpiceBotTest", target)
                    bot.db.set_nick_value(target, 'spicebothour_warn', 'true')

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
