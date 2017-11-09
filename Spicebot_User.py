import sopel.module
from sopel import module, tools
from sopel.module import ADMIN
from sopel.module import event, rule
from sopel.module import OP
from sopel.tools.target import User, Channel
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
LASTTIMEOUTHOUR = 3600

@sopel.module.commands('spicebot')
def mainfunction(bot, trigger):
    inchannel = trigger.sender
    if trigger.group(2):
        allowedcommandsarray = ['on','off']
        commandused = trigger.group(3)
        if commandused in allowedcommandsarray:
            execute_main(bot, trigger)
        elif not inchannel.startswith("#"):
            execute_main(bot, trigger)
        else:
            enablestatus = spicebot_prerun(bot, trigger)
            if not enablestatus:
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
    options = str("options, warn, channel, modulecount, owner, github, timeout, usage, status, on/off, isadmin, isop")
    if not trigger.group(2):
        bot.say("That's my name. Don't wear it out!")
    else:
        commandused = trigger.group(3)
        
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
            
        ## Is OP
        elif commandused == 'isop':
            target = trigger.group(4)
            if not target:
                target = trigger.nick
            if target not in bot.privileges[channel]:
                bot.say("I'm not sure who that is.")
            else:
                if bot.privileges[channel][target] == OP:
                    bot.say(target + ' is an op.')
                else:
                    bot.say(target + ' is not an op.')
            
        ## Is Admin
        elif commandused == 'isadmin':
            target = trigger.group(4)
            if not target:
                target = trigger.nick
            if target not in bot.privileges[channel]:
                bot.say("I'm not sure who that is.")
            else:
                if target != instigator:
                    bot.say("Work in progress.")
                elif trigger.admin:
                    bot.say(target + ' is a bot admin.')
                else:
                    bot.say(target + ' is not a bot admin.')
        
        ## How long does a user have to wait to use a command
        elif commandused == 'timeout'and not inchannel.startswith("#"):
            target = trigger.group(4)
            if not target:
                target = trigger.nick
            if target not in bot.privileges[channel]:
                bot.say("I'm not sure who that is.")
            elif target == instigator or trigger.admin:
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
        elif commandused == 'usage'and not inchannel.startswith("#"):
            target = trigger.group(4)
            if not target:
                target = trigger.nick
            if target == instigator or trigger.admin:
                usertotal = get_usertotal(bot, target)
                message = str(target + " has used " + str(usertotal) + " commands this hour.")
            else:
                message = str(target + ", you can't check other's usage.")
            bot.notice(message, instigator)
            
        ## Enable/Disable status
        elif commandused == 'status'and not inchannel.startswith("#"):
            target = trigger.group(4)
            if not target:
                target = trigger.nick
            if target == '':
                target = trigger.nick
            disenable = get_disenable(bot, target)
            if disenable:
                message = str(target + " has SpiceBot enabled")
            else:
                message = str(target + " does not have SpiceBot enabled")
            bot.notice(message, instigator)
        
        ## Resets
        elif commandused.startswith('timereset') and trigger.admin:
            target = commandused.replace('timereset','').strip()
            if target == '':
                target = trigger.nick
            bot.say('resetting timeout for ' + target)
            reset_timeout(bot, target)
        elif commandused.startswith('warnreset') and trigger.admin:
            target = commandused.replace('warnreset','').strip()
            if target == '':
                target = trigger.nick
            bot.say('resetting warning for ' + target)
            reset_warn(bot, target)
        elif commandused.startswith('countreset') and trigger.admin:
            target = commandused.replace('countreset','').strip()
            if target == '':
                target = trigger.nick
            bot.say('resetting count for ' + target)
            reset_count(bot, target)
            
        ## On/Off
        elif commandused.startswith('on') or commandused.startswith('off'):
            if commandused.startswith('on'):
                target = str(commandused.split("on", 1)[1]).strip()
                #target = commandused.replace('on','').strip()
                statuschange = 'enabl'
            else:
                #target = commandused.replace('off','').strip()
                target = str(commandused.split("off", 1)[1]).strip()
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

## Auto Mod
@event('JOIN','PART','QUIT','NICK')
@rule('.*')
def greeting(bot, trigger):
    target = trigger.nick
    set_jointime(bot, target)
    lasttime = get_lasttime(bot, target)
    if not lasttime or lasttime < LASTTIMEOUTHOUR:
        bot.db.set_nick_value(target, 'spicebot_usertotal', '')
        bot.db.set_nick_value(target, 'spicebothour_warn', '')

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
