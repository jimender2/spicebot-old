import sopel.module
import random
import urllib

fra='https://raw.githubusercontent.com/deathbybandaid/sopel-modules/dev/otherfiles/ferengi_rules.txt'

@sopel.module.commands('ferengi')
def ferengi(bot, trigger):
    if not trigger.group(2):
        myline = randomfra()
    else:
        myline = specificrule()
    bot.say(myline)

# random rule
def randomfra():
    htmlfile=urllib.urlopen(fra)
    lines=htmlfile.read().splitlines()
    myline=random.choice(lines)
    if not myline or myline == '\n':
        myline = randomfra()
    return myline

# rule number
def specificrule():
    rulenumber = int(trigger.group(2))
    htmlfile=urllib.urlopen(fra)
    lines=htmlfile.readlines()
    try:
        myline = str(lines[rulenumber-1])
    except IndexError:
        myline = 'That doesnt appear to be a rule number.'
    if not myline or myline == '\n':
        myline = 'There is no cannonized rule tied to this number.'
