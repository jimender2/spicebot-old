import sopel.module
import urllib

rulesurl = 'https://pastebin.com/raw/Vrq9bHBD'

@sopel.module.commands('rulesa','rulea')
def rules(bot, trigger):
        if not trigger.group(2):
                bot.say('Chat Rules:     https://pastebin.com/Vrq9bHBD')
        else:
                rulenumber = trigger.group(2)
                htmlfile=urllib.urlopen(rulesurl)
                lines=htmlfile.readlines()
                mylines=lines[str(rulenumber)]
                bot.say(myline)
