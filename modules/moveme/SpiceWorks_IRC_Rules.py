#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib
from word2number import w2n
import sys
import os

rulesurl = 'https://pastebin.com/raw/Vrq9bHBD'

@sopel.module.commands('rules','rule')
def execute_main(bot, trigger):
    rulenumber = trigger.group(2)
    if not rulenumber:
        myline='Chat Rules:     https://pastebin.com/Vrq9bHBD'
    else:
        if not rulenumber[0].isdigit():
            rulenumber = w2n.word_to_num(str(rulenumber))
        else:
            rulenumber = int(rulenumber)
    
        htmlfile=urllib.urlopen(rulesurl)
        lines=htmlfile.readlines()
        try:
            if str(rulenumber) != '0':
                myline=lines[rulenumber-1]
            else:
                myline='Rule Zero (read the rules):     https://pastebin.com/Vrq9bHBD'
        except IndexError or TypeError:
            if rulenumber == 69:
                myline='giggles'
            elif rulenumber == 34:
                myline='If it exists, there is porn of it.'
            else:
                myline= 'That doesnt appear to be a rule number.'

        if myline == 'giggles':
            bot.action(myline)
        else:
            bot.say(myline)
