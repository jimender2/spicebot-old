import sopel.module
import urllib
from word2number import w2n

rulesurl = 'https://pastebin.com/raw/Vrq9bHBD'

@sopel.module.rate(120)
@sopel.module.commands('rules','rule')
def rules(bot, trigger):
    if not trigger.group(2):
        myline='Chat Rules:     https://pastebin.com/Vrq9bHBD'
    else:
        rulenumber = trigger.group(2)
        if not rulenumber.isdigit():
            try:
                rulenumber = w2n.word_to_num(str(rulenumber))
            except ValueError:
                bot.say('That does not appear to be a vialid number.')
        else:
            rulenumber = int(rulenumber)
        
        htmlfile=urllib.urlopen(rulesurl)
        lines=htmlfile.readlines()
        try:
            if rulenumber != '0':
                myline=lines[rulenumber-1]
        except IndexError:
            if rulenumber == 0:
                myline='Rule Zero (read the rules):     https://pastebin.com/Vrq9bHBD'
            elif rulenumber == 69:
                myline='giggles'
            elif rulenumber == 34:
                myline='If it exists, there is porn of it.'
            else:
                myline= 'That doesnt appear to be a rule number.'
    
    if myline == 'giggles':
            bot.action(myline)
    else:
            bot.say(myline)
