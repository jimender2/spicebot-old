import sopel
from sopel import module, tools
import random

@sopel.module.rate(120)
@sopel.module.commands('webmd','webmdadd','webmddel')
@module.require_chanmsg
def webmd(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    targetdisenable = get_spicebotdisenable(bot, target)
    if targetdisenable:
        commandtrimmed = trigger.group(1)
        commandtrimmed = str(commandtrimmed.split("webmd", 1)[1])
        webmd = get_webmd(bot)
        if commandtrimmed == '':
            target = trigger.group(3) or trigger.nick
            responses  = ["has died from","is being treated for","is recovering from"]
            reply = random.randint(0,len(responses) - 1)
            condition = str(responses [reply])
            try:
                result =random.choice(webmd)
            except IndexError:
                result = "death"
            conclusion = str(target + ' ' + condition + ' ' + result + '.')
            bot.say(conclusion)
        elif not trigger.group(2):
            bot.say("What would you like to add/remove?")
        else:
            webmdchange = str(trigger.group(2))
            if commandtrimmed == 'add':
                if webmdchange in webmd:
                    bot.say(webmdchange + " is already in the webmd locker.")
                    rescan = 'False'
                else:
                    webmd.append(webmdchange)
                    update_webmd(bot, webmd)
                    rescan = 'True'
            elif commandtrimmed == 'del':
                if webmdchange not in webmd:
                    bot.say(webmdchange + " is not in the webmd locker.")
                    rescan = 'False'
                else:
                    webmd.remove(webmdchange)
                    update_webmd(bot, webmd)
                    rescan = 'True'
            if rescan == 'True':
                webmd = get_webmd(bot)
                if webmdchange in webmd:
                    bot.say(webmdchange + " has been added to the webmd locker.")
                else:
                    bot.say(webmdchange + ' has been removed from the webmd locker.')
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)

def get_webmd(bot):
    for channel in bot.channels:
        webmd = bot.db.get_nick_value(channel, 'webmd_locker') or []
        return webmd
        
def update_webmd(bot, webmd):
    for channel in bot.channels:
        bot.db.set_nick_value(channel, 'webmd_locker', webmd)

def update_usertotal(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)

## Check Status of Opt In
def get_spicebotdisenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
