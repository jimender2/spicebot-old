import sopel.module
import sys, re
from num2words import num2words

@sopel.module.rate(120)
@sopel.module.commands('ERMAHGERD')
def ERMAHGERD(bot,trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if trigger.group(2):
            ernpert = trigger.group(2)
            spertitert = trernslert(ernpert)
            bot.say('ERMAHGERD,' + str(spertitert))
        else:
            bot.say('Whert der yer wernt ter trernslert?')
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
        
def trernslert(werds):
    terkerns = werds.split()
    er = ''
    for terk in terkerns:
        
        if terk.endswith(','):
            terk = re.sub(r"[,]+", '', terk)
            cermmer = 'true'
        else:
            cermmer = 'false'

        if terk.startswith('('):
            terk = re.sub(r"[(]+", '', terk)
            lerftperernthersers = 'true'
        else:
            lerftperernthersers = 'false'
        
        if terk.endswith(')'):
            terk = re.sub(r"[)]+", '', terk)
            rerghtperernthersers = 'true'
        else:
            rerghtperernthersers = 'false'
            
        if terk.endswith('%'):
            terk = re.sub(r"[%]+", '', terk)
            percernt = 'true'
        else:
            percernt = 'false'

        werd = ermergerd(terk)
        
        if lerftperernthersers == 'true':
            werd = str('(' + werd)
        
        if percernt == 'true':
            werd = str(werd + ' PERCERNT')
        
        if rerghtperernthersers == 'true':
            werd = str(werd + ')')
        
        if cermmer == 'true':
            werd = str(werd + ',')
        cermmer
        
        er = er + ' ' + werd
    return er
    
def ermergerd(w):
    w = w.strip().lower()
    derctshernerer = {'me':'meh','you':'u', 'are':'er', "you're":"yer", "i'm":"erm", "i've":"erv", "my":"mah", "the":"da", "omg":"ermahgerd"}
    if w in derctshernerer:
        return derctshernerer[w].upper()
    else:
        w = re.sub(r"[\.,/;:!@#$%^&*\?)(]+", '', w)
        if w[0].isdigit():
            w = num2words(int(w))
        w = re.sub(r"tion", "shun", w)
        pat = r"[aeiouy]+"
        er =  re.sub(pat, "er", w)
        if w.startswith('y'):
            er = 'y' + re.sub(pat, "er", w[1:])
        if w.endswith('e') and not w.endswith('ee') and len(w)>3:
            er = re.sub(pat, "er", w[:-1]) 
        if w.endswith('ing'):
            er = re.sub(pat, "er", w[:-3]) + 'in'
        er = er[0] + er[1:].replace('y', 'er')
        er = er.replace('rr', 'r')
        return er.upper()

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
