import sopel.module
import urllib

rulesurl = 'https://pastebin.com/raw/Vrq9bHBD'

@sopel.module.commands('rulesa','rulea')
def rules(bot, trigger):
        rulenumber = int(trigger.group(2))
        if not trigger.group(2):
                bot.say('Chat Rules:     https://pastebin.com/Vrq9bHBD')
        else:
                htmlfile=urllib.urlopen(rulesurl)
                lines=htmlfile.readlines()
                myline=lines[rulenumber-1]
                bot.say(myline)
                bot.say(rulenumber)
