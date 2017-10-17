import sopel.module
import random
import urllib

fra='https://raw.githubusercontent.com/deathbybandaid/sopel-modules/dev/otherfiles/ferengi_rules.txt'

@sopel.module.rate(120)
@sopel.module.commands('ferengi')
def ferengi(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if not trigger.group(2):
            myline = randomfra()
        else:
            rulenumber = int(trigger.group(2))
            htmlfile=urllib.urlopen(fra)
            lines=htmlfile.readlines()
            try:
                myline = str(lines[rulenumber-1])
            except IndexError:
                myline = 'That doesnt appear to be a rule number.'
            if not myline or myline == '\n':
                myline = 'There is no cannonized rule tied to this number.'
        bot.say(myline)
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
# random rule
def randomfra():
    htmlfile=urllib.urlopen(fra)
    lines=htmlfile.read().splitlines()
    myline=random.choice(lines)
    if not myline or myline == '\n':
        myline = randomfra()
    return myline

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
