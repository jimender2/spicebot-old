import sopel.module
import urllib

rulesurl = 'https://pastebin.com/raw/Vrq9bHBD'

@sopel.module.commands('rulesa','rulea')
def rules(bot, trigger):
        if not trigger.group(2):
                bot.say('Chat Rules:     https://pastebin.com/Vrq9bHBD')
        else:
                rulenumber = str(trigger.group(2))
                htmlfile=urllib.urlopen(rulesurl)
                lines=htmlfile.readlines()
                myline=lines[rulenumber]
                bot.say(myline)
                bot.say(rulenumber)
