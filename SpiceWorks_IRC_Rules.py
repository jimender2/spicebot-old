import sopel.module
import urllib
from word2number import w2n

rulesurl = 'https://pastebin.com/raw/Vrq9bHBD'

@sopel.module.rate(120)
@sopel.module.commands('rules','rule')
def rules(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if not trigger.group(2):
            myline='Chat Rules:     https://pastebin.com/Vrq9bHBD'
        else:
            rulenumber = trigger.group(2)
            if not rulenumber[0].isdigit():
                rulenumber = w2n.word_to_num(str(rulenumber))
            else:
                rulenumber = int(rulenumber)
        
            htmlfile=urllib.urlopen(rulesurl)
            lines=htmlfile.readlines()
            try:
                if str(rulenumber) != '0':
                    myline=lines[rulenumber-1]
                else:
                    myline='Rule Zero (read the rules):     https://pastebin.com/Vrq9bHBD'
            except IndexError or TypeError:
                if rulenumber == 69:
                    myline='giggles'
                elif rulenumber == 34:
                    myline='If it exists, there is porn of it.'
                else:
                    myline= 'That doesnt appear to be a rule number.'
    
            if myline == 'giggles':
                bot.action(myline)
            else:
                bot.say(myline)
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)

def update_usertotal(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)
        
## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
