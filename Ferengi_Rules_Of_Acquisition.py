import sopel.module
import random
import urllib

fra='https://raw.githubusercontent.com/deathbybandaid/sopel-modules/dev/otherfiles/ferengi_rules.txt'

@sopel.module.commands('ferengi')
def ferengi(bot, trigger):
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

# random rule
def randomfra():
    htmlfile=urllib.urlopen(fra)
    lines=htmlfile.read().splitlines()
    myline=random.choice(lines)
    return myline
