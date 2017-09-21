import sopel.module
import random
import urllib

@sopel.module.commands('ferengi')
def ferengi(bot, trigger):
    fra='https://raw.githubusercontent.com/deathbybandaid/sopel-modules/dev/otherfiles/ferengi_rules.txt'
    if not trigger.group(2):
        htmlfile=urllib.urlopen(fra)
        lines=htmlfile.read().splitlines()
        myline=random.choice(lines)
    else:
        rulenumber = int(trigger.group(2))
        htmlfile=urllib.urlopen(fra)
        lines=htmlfile.readlines()
        try:
            myline=lines[rulenumber-1]
        except IndexError:
            myline= 'That doesnt appear to be a rule number.'
    
    if not myline:
        myline = 'There is no cannonized rule tied to this number.'
    bot.say(myline)
