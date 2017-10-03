import sopel.module
import sys, re
from num2words import num2words

@sopel.module.rate(120)
@sopel.module.commands('ERMAHGERD')
def ERMAHGERD(bot,trigger):
    if trigger.group(2):
        ernpert = trigger.group(2)
        spertitert = trernslert(ernpert)
        bot.say('ERMAHGERD,' + str(spertitert))
    else:
        bot.say('Whert der yer wernt ter trernslert?')

def trernslert(werds):
    terkerns = werds.split()
    er = ''
    for terk in terkerns:

        if terk.startswith('('):
            terk = re.sub(r"[(]+", '', terk)
            lerftperernthersers = 'true'
        else:
            lerftperernthersers = 'false'
        
        if terk.endswith(')'):
            terk = re.sub(r"[(]+", '', terk)
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
