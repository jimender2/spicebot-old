import sopel.module
import urllib

rulesurl = 'https://pastebin.com/raw/Vrq9bHBD'

@sopel.module.commands('rulesa','rulea')
def rules(bot, trigger):
        rulenumber = trigger.group(2)
        actualrulenumber = rulenumber - 1
        if not trigger.group(2):
                bot.say('Chat Rules:     https://pastebin.com/Vrq9bHBD')
        else:
                htmlfile=urllib.urlopen(rulesurl)
                lines=htmlfile.readlines()
                myline=lines[3]
                bot.say(myline)
                bot.say(actualrulenumber)
