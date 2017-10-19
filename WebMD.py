import sopel
from sopel import module, tools

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
            try:
                result =random.choice(webmd)
            except IndexError:
                result = "immediate death"
            bot.say(result)
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
