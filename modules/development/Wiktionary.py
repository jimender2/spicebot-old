# coding=utf-8
# wiktionary.py - Sopel/SpiceBot Wiktionary Module
# Copyright 2009, Sean B. Palmer, inamidst.com
# Licensed under the Eiffel Forum License 2.
# Modified to conform to SpiceBot Prerun checks 2018, Dyson M. N. Parkes

from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel.module import commands, example, NOLIMIT
import random
import sys
import os
import requests
import re
import urllib
import urllib2
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

## Global variables
uri = 'http://en.wiktionary.org/w/index.php?title=%s&printable=yes'
r_tag = re.compile(r'<[^>]+>')
r_ul = re.compile(r'(?ims)<ul>.*?</ul>')

@commands('define', 'dict','dictionary')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'define')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    word = trigger.group(2)
    if word is None:
        bot.reply('You must tell me what to look up!')
        return
    _etymology, definitions = wikt(word)
    if not definitions:
        bot.say("Couldn't get any definitions for %s." % word)
        return
    result = format(word, definitions)
    if len(result) < 150:
        result = format(word, definitions, 3)
    if len(result) < 150:
        result = format(word, definitions, 5)

    if len(result) > 300:
        result = result[:295] + '[...]'
    bot.say(result)

def text(html):
    text = r_tag.sub('', html).strip()
    text = text.replace('\n', ' ')
    text = text.replace('\r', '')
    text = text.replace('(intransitive', '(intr.')
    text = text.replace('(transitive', '(trans.')
    return text

def wikt(word):
    bytes = requests.get(uri % quote(word))
    bytes = r_ul.sub('', bytes)

    mode = None
    etymology = None
    definitions = {}
    for line in bytes.splitlines():
        if 'id="Etymology"' in line:
            mode = 'etymology'
        elif 'id="Noun"' in line:
            mode = 'noun'
        elif 'id="Verb"' in line:
            mode = 'verb'
        elif 'id="Adjective"' in line:
            mode = 'adjective'
        elif 'id="Adverb"' in line:
            mode = 'adverb'
        elif 'id="Interjection"' in line:
            mode = 'interjection'
        elif 'id="Particle"' in line:
            mode = 'particle'
        elif 'id="Preposition"' in line:
            mode = 'preposition'
        elif 'id="' in line:
            mode = None

        elif (mode == 'etmyology') and ('<p>' in line):
            etymology = text(line)
        elif (mode is not None) and ('<li>' in line):
            definitions.setdefault(mode, []).append(text(line))

        if '<hr' in line:
            break
    return etymology, definitions

parts = ('preposition', 'particle', 'noun', 'verb',
    'adjective', 'adverb', 'interjection')

def format(result, definitions, number=2):
    for part in parts:
        if part in definitions:
            defs = definitions[part][:number]
            result += u' — {}: '.format(part)
            n = ['%s. %s' % (i + 1, e.strip(' .')) for i, e in enumerate(defs)]
            result += ', '.join(n)
    return result.strip(' .,')

def quote(string, safe='/'):
    """Like urllib2.quote but handles unicode properly."""
    if sys.version_info.major < 3:
        if isinstance(string, unicode):
            string = string.encode('utf8')
        string = urllib.quote(string, safe.encode('utf8'))
    else:
        string = urllib.parse.quote(str(string), safe)
    return string
