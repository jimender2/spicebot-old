import sopel.module
import urllib
import linecache

rulesurl = 'https://pastebin.com/Vrq9bHBD'

@sopel.module.commands('rulesa','rulea')
def rules(bot, input):
        if not trigger.group(2):
                bot.say('Chat Rules:     https://pastebin.com/Vrq9bHBD')
        else:
                rulenumber = trigger.group(2).strip()
                htmlfile=urllib.urlopen(fra)
                lines=htmlfile.read().splitlines()
                myline=linecache.getline(lines, rulenumber)
                bot.say(myline)
