import sopel.module
from sopel import module, tools
from sopel.module import ADMIN
from sopel.module import VOICE
from sopel.module import event, rule
from sopel.module import OP
from sopel.tools.target import User, Channel
import time
import os
import sys
import fnmatch
import re
import git 
from os.path import exists
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

log_path = "data/templog.txt"
log_file_path = os.path.join(moduledir, log_path)

OPTTIMEOUT = 1800
FINGERTIMEOUT = 1800
TOOMANYTIMES = 15
LASTTIMEOUT = 60
LASTTIMEOUTHOUR = 3600

GITWIKIURL = "https://github.com/deathbybandaid/sopel-modules/wiki"

validsubcommandarray = ['options','docs','help','warn','channel','modulecount','isowner','isop','isvoice','isadmin','on','off','isonforwho','timeout','usage']

statsadminarray = ['hourwarned','usertotal','lastopttime','disenable']

@sopel.module.commands('spicebot','spicebotadmin')
def main_command(bot, trigger):
    now = time.time()
    service = bot.nick.lower()
    maincommandused = trigger.group(1)
    triggerargsarray = create_args_array(trigger.group(2))
    subcommand = get_trigger_arg(triggerargsarray, 1)
    instigator = trigger.nick
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray, channel = special_users(bot)
    optedinarray, targetcantoptarray = [], []
    for u in allusersinroomarray:
        disenable = get_botdatabase_value(bot, u, 'disenable')
        if u != bot.nick and disenable:
            optedinarray.append(u)
        opttime = get_timesince(bot, u, 'opttime')
        if opttime < OPTTIMEOUT and not bot.nick.endswith(devbot):
            targetcantoptarray.append(u)
    inchannel = trigger.sender
    commandlist = get_trigger_arg(validsubcommandarray, "list")
    if not subcommand:
        bot.say("That's my name. Don't wear it out!")
    elif subcommand not in validsubcommandarray and instigator not in adminsarray:
        bot.say("Invalid command. Options are: " + commandlist +".")
    
    ## Options
    elif subcommand == 'options':
        bot.say("Options are: " + commandlist +".")
        
    ## Docs
    elif subcommand == 'help' or subcommand == 'docs':
        bot.notice(instigator + ", Online Docs: " + GITWIKIURL, instigator)
        
    ## Warn against Bot abuse
    elif subcommand == 'warn':
        target = get_trigger_arg(triggerargsarray, 2) or ''
        bot.msg(channel, target + "This is just a warning. Overuse of the bot, can get you kicked or banned by an operator. If you want to purely play with the bot, go to ##SpiceBotTest, or send Spicebot a PrivateMessage.")
        
    ## Channel
    elif subcommand == 'channel':
        bot.say("You can find me in " + channel)
    
    ## Github Repo
    elif subcommand == 'github':
        bot.say('Spiceworks IRC Modules     https://github.com/deathbybandaid/sopel-modules')
    
    ## Modules
    elif subcommand == 'modulecount':
        modulecount = str(len(fnmatch.filter(os.listdir(moduledir), '*.py')))
        bot.say('There are currently ' + modulecount +' custom modules installed.')
        
    ## Bot Owner
    elif subcommand == 'isowner':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif target in botownerarray:
            bot.say(target + ' is the owner.')
        else:
            bot.say(target + ' is not the owner.')
    
    ## Bot Admin
    elif subcommand == 'isadmin':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif target in adminsarray:
            bot.say(target + ' is a bot admin.')
        else:
            bot.say(target + ' is not a bot admin.')
            
    ## Chan OP
    elif subcommand == 'isop':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif target in operatorarray:
            bot.say(target + ' is OP.')
        else:
            bot.say(target + ' is not OP.')
                        
    ## Chan VOICE
    elif subcommand == 'isvoice':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif target in voicearray:
            bot.say(target + ' is VOICE.')
        else:
            bot.say(target + ' is not VOICE.')
        
    ## On/off
    elif subcommand == 'on' or subcommand == 'off':
        disenablevalue = None
        if commandortarget == 'on':
            disenablevalue = 1
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        targetopttime = get_timesince(bot, target, 'opttime')
        if target.lower() not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif target.lower() not in allusersinroomarray and target != 'everyone':
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif target != instigator and instigator not in adminsarray:
            bot.notice(instigator + "This is an admin only function.", instigator)
        elif target == 'everyone':
            for u in allusersinroomarray:
                set_botdatabase_value(bot, u, 'disenable', disenablevalue)
            bot.notice(instigator + ", " + bot.nick + " should now be " +  commandortarget + ' for ' + target + '.', instigator)
        elif target in targetcantoptarray:
            bot.notice(instigator + " It looks like " + target + " can't enable/disable " + bot.nick + " for %d seconds." % (OPTTIMEOUT - targetopttime), instigator)
        elif commandortarget == 'on' and target.lower() in optedinarray:
            bot.notice(instigator + ", It looks like " + target + " already has " + bot.nick + " on.", instigator)
        elif commandortarget == 'off' and target.lower() not in optedinarray:
            bot.notice(instigator + ", It looks like " + target + " already has " + bot.nick + " off.", instigator)
        else:
            set_botdatabase_value(bot, target, 'disenable', disenablevalue)
            set_botdatabase_value(bot, target, 'opttime', now)
            bot.notice(instigator + ", " + bot.nick + " should now be " +  commandortarget + ' for ' + target + '.', instigator)
    
    ## who is the bot on for
    elif subcommand == 'isonforwho' and inchannel.startswith("#"):
        bot.say('This command can only be run in privmsg.')
    elif subcommand == 'isonforwho' and not inchannel.startswith("#"):
        targetline = get_trigger_arg(optedinarray, "list") or ''
        chunks = targetarray.split()
        per_line = 15
        for i in range(0, len(chunks), per_line):
            targetline = " ".join(chunks[i:i + per_line])
            bot.say(str(targetline))
        if targetline == '':
            bot.say('Nobody has ' + bot.nick + " enabled.")
    
    ## usage
    elif subcommand == 'usage':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target.lower() not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        else:
            usertotal = get_botdatabase_value(bot, target, 'usertotal')
            bot.say(target + " has used " + str(usertotal) + " commands this hour.")
    
    ## timeout
    elif subcommand == 'timeout':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target.lower() not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        else:
            lasttime = get_timesince(bot, target, 'lastusagetime')
            if lasttime < LASTTIMEOUT:
                lasttimemath = int(LASTTIMEOUT - lasttime)
                message = str(target + " needs to wait " + str(lasttimemath) + " seconds to use Spicebot.")
            else:
                message = str(target + " should be able to use SpiceBot")
            bot.say(message)
    
    ## bot status
    elif subcommand == 'status':
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if target.lower() not in allusersinroomarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        else:
            disenable = get_botdatabase_value(bot, target, 'disenable')
            if disenable:
                message = str(target + " has SpiceBot enabled")
            else:
                message = str(target + " does not have SpiceBot enabled")
            bot.say(message)
    
###### admin only block 
    elif instigator not in adminsarray:
        bot.notice(instigator + "This is an admin only function.", instigator)
    
    ## do a /me action for the bot in channel
    elif subcommand == 'chanaction':
        message = get_trigger_arg(triggerargsarray, '2+')
        if message:
            bot.action(message,channel)
    
    ## Make the bot talk in channel
    elif subcommand == 'chanmsg':
        message = get_trigger_arg(triggerargsarray, '2+')
        if message:
            bot.msg(channel,message)
    
    ## set and reset values
    elif subcommand == 'statsadmin':
        incorrectdisplay = "A correct command use is .spicebotadmin statsadmin target set/reset stat"
        target = get_trigger_arg(triggerargsarray, 2)
        subcommand = get_trigger_arg(triggerargsarray, 3)
        statset = get_trigger_arg(triggerargsarray, 4)
        newvalue = get_trigger_arg(triggerargsarray, 5) or None
        if not target:
            bot.notice(instigator + ", Target Missing. " + incorrectdisplay, instigator)
        elif target.lower() not in allusersinroomarray and target != 'everyone':
            bot.notice(instigator + ", It looks like " + str(target) + " is either not here, or not a valid person.", instigator)
        elif not subcommand:
            bot.notice(instigator + ", Subcommand Missing. " + incorrectdisplay, instigator)
        elif subcommand not in statsadminchangearray:
            bot.notice(instigator + ", Invalid subcommand. " + incorrectdisplay, instigator)
        elif not statset:
            bot.notice(instigator + ", Stat Missing. " + incorrectdisplay, instigator)
        elif statset not in statsadminarray and statset != 'all':
            bot.notice(instigator + ", Invalid stat. " + incorrectdisplay, instigator)
        elif instigator not in adminsarray:
            bot.notice(instigator + "This is an admin only function.", instigator)
        else:
            if subcommand == 'reset':
                newvalue = None
            if subcommand == 'set' and newvalue == None:
                bot.notice(instigator + ", When using set, you must specify a value. " + incorrectdisplay, instigator)
            elif target == 'everyone':
                for u in bot.channels[channel].users:
                    if statset == 'all':
                        for x in statsadminarray:
                            set_botdatabase_value(bot, u, x, newvalue)
                    else:
                        set_botdatabase_value(bot, u, statset, newvalue)
                bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)
            else:
                if statset == 'all':
                    for x in statsadminarray:
                        set_botdatabase_value(bot, target, x, newvalue)
                else:
                    set_botdatabase_value(bot, target, statset, newvalue)
                bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)

    ## Update from github
    elif subcommand == 'update':
        bot.msg(channel, trigger.nick + " commanded me to update from Github and restart. Be Back Soon!")
        update(bot, trigger)
        restart(bot, trigger, service)
    
    ## restart the bot's service
    elif subcommand == 'restart':
        bot.msg(channel, trigger.nick + " Commanded me to restart. Be Back Soon!")
        restart(bot, trigger, service)   
                
    ## install a python pip package
    elif subcommand == 'pipinstall':
        pippackage = get_trigger_arg(triggerargsarray, '2+')
        if not pippackage:
            bot.say("You must specify a pip package")
        else:
            bot.say("attempting to install " + pippackage)
            os.system("sudo pip install " + pippackage)
            bot.say('Possibly done installing ' + pippackage)      
                
    elif subcommand == 'debug':
        debugloglinenumberarray = []
        bot.action('Is Copying Log')
        os.system("sudo journalctl -u " + service + " >> " + log_file_path)
        bot.action('Is Filtering Log')
        search_phrase = "Welcome to Sopel. Loading modules..."
        ignorearray = ['session closed for user root','COMMAND=/bin/journalctl','COMMAND=/bin/rm','pam_unix(sudo:session): session opened for user root']
        mostrecentstartbot = 0
        with open(log_file_path) as f:
            line_num = 0
            for line in f:
                line_num += 1
                if search_phrase in line:
                    mostrecentstartbot = line_num
            line_num = 0
        with open(log_file_path) as fb:
            for line in fb:
                line_num += 1
                currentline = line_num
                if int(currentline) >= int(mostrecentstartbot) and not any(x in line for x in ignorearray):
                    bot.say(line)
        bot.action('Is Removing Log')
        os.system("sudo rm " + log_file_path)

def restart(bot, trigger, service):
    bot.say('Restarting Service...')
    os.system("sudo service " + str(service) + " restart")
    bot.say('If you see this, the service is hanging. Making another attempt.')

def update(bot, trigger):
    bot.say('Pulling From Github...')
    g = git.cmd.Git(moduledir)
    g.pull()
    
    
    
    
