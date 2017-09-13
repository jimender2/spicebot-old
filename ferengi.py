import sopel.module
import random
import urllib

@sopel.module.commands('ferengi')
def ferengi(bot, trigger):
        fra='https://gist.githubusercontent.com/deathbybandaid/cf1faedb87098224943dc04453bc3f79/raw/5ef59ed209f580bf0a7885945e816445aea178e3/gistfile1.txt'
        htmlfile=urllib.urlopen(fra)
        lines=htmlfile.read().splitlines()
        myline=random.choice(lines)
        bot.say(myline)
