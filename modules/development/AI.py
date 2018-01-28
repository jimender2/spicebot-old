"""
ai.py - Artificial Intelligence Module
Copyright 2009-2011, Michael Yanovich, yanovich.net
Modified 2018 to conform to SpiceBot preflight, DysonParkes
Licensed under the Eiffel Forum License 2.
http://sopel.chat
How often the bot joins in is controlled by 'rate'. This is calculated by 'frequency' / 10
Several functions seem to have a sleep period built in. Once they're understood they'll be commented.
"""
from sopel.module import rule, priority, rate
import random
import time

from SpicebotShared import *

@sopel.module.commands('ai')
def mainfunction(bot, trigger): # dummy function to allow module to load at present.  
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'ai')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray): # Response for running the dummy command directly
    commandused = get_trigger_arg(triggerargsarray, 1)
    # adminusers array, triggerargsarray
    if commandused == 'channels':
        channels = bot.config.ai.valid_channels
        bot.say(str(channels))
    # if adminuser:
    # if triggerarg1 = enable, add channel to bot.config.ai.active_channels
    # if triggerarg1 = disable, remove channel from bot.config.ai.active_channels
    else:
        bot.say("It's not intelligence if you're telling me to do it directly.")
    
    
def setup(bot): # Check to see if bot is configured
    if bot.config.ai and bot.config.ai.frequency and bot.config.ai.active_channels: 
        bot.memory['frequency'] = bot.config.ai.frequency # Pull 'frequency' from bot config into memory if configured
        bot.memory['valid_channels'] = bot.config.ai.valid_channels or '' # Confirm valid channels
    else:
        bot.memory['frequency'] = 3 # Set frequency to 3 if not configured in config
        bot.memory['valid_channels'] = ''

    random.seed() # initialise random number

def decide(bot):
    return 0 < random.random() < float(bot.memory['frequency']) / 10

@rule('(?i)$nickname\:\s+(bye|goodbye|gtg|seeya|cya|ttyl|g2g|gnight|goodnight)') # Things to respond to
@rate(30)
def goodbye(bot, trigger):
    byemsg = random.choice(('Bye', 'Goodbye', 'Seeya', 'Auf Wiedersehen', 'Au revoir', 'Ttyl')) # Response options
    punctuation = random.choice(('!', ' ', '.')) # Punctuation options
    bot.say(byemsg + ' ' + trigger.nick + punctuation) # Say response + instigator + punctuation

@rule('(?i).*(thank).*(you).*(sopel|$nickname).*$') # Respond to 'thank you botnick'
@rate(30)
@priority('high')
def ty(bot, trigger): # Function name "ty"
    human = random.uniform(0, 9) # Random number with uniform chances across range
    time.sleep(human) # Wait for random time
    mystr = trigger.group() # Retrieve what was said
    mystr = str(mystr) # Cast what was said as string
    if (mystr.find(" no ") == -1) and (mystr.find("no ") == -1) and (mystr.find(" no") == -1): # Make sure it wasn't "no thank you"
        bot.reply("You're welcome.") # Reply

@rule('(?i)$nickname\:\s+(thank).*(you).*') # Respond to "thank you"
@rate(30)
def ty2(bot, trigger):
    ty(bot, trigger) # Activate function "ty"

@rule('(?i).*(thanks).*(sopel|$nickname).*') # Respond to "thanks botnick"
@rate(40)
def ty4(bot, trigger):
    ty(bot, trigger) # Activate function "ty"

@rule('(sopel|$nickname)\:\s+(yes|no)$') # Respond to "botnick: yes/no"
@rate(15)
def yesno(bot, trigger):
    rand = random.uniform(0, 5) # Random time to wait
    text = trigger.group()
    text = text.split(":")
    text = text[1].split()
    time.sleep(rand) # wait a moment
    if text[0] == 'yes': # just disagree
        bot.reply("no")
    elif text[0] == 'no': # just disagree
        bot.reply("yes")

@rule('(?i)($nickname|sopel)\:\s+(ping)\s*') # Respond to botnick: ping
@rate(30)
def ping_reply(bot, trigger):
    text = trigger.group().split(":")
    text = text[1].split()
    if text[0] == 'PING' or text[0] == 'ping':
        bot.reply("PONG")

@rule('(?i)((sopel|$nickname)\[,:]\s*i.*love|i.*love.*(sopel|$nickname).*)') # Respond to "I love botnick"
@rate(30)
def love(bot, trigger):
    bot.reply("I love you too.") # Respond

@rule('\s*([Xx]+[dD]+|([Hh]+[Aa]+)+)') # Respond to: xd, ha (upper/lower irrelevant)
@rate(30)
def xd(bot, trigger):
    respond = ['xDDDDD', 'XD', 'XDDDD', 'haha'] # Response options
    randtime = random.uniform(0, 3) # Time to wait
    time.sleep(randtime) # Wait a bit
    bot.say(random.choice(respond)) # Respond

@rule('(haha!?|lol!?)$')
@priority('high')
def f_lol(bot, trigger):
    if decide(bot):
        respond = ['haha', 'lol', 'rofl', 'hm', 'hmmmm...']
        randtime = random.uniform(0, 9)
        time.sleep(randtime)
        bot.say(random.choice(respond))

@rule('^\s*(([Bb]+([Yy]+[Ee]+(\s*[Bb]+[Yy]+[Ee]+)?)|[Ss]+[Ee]{2,}\s*[Yy]+[Aa]+|[Oo]+[Uu]+)|cya|ttyl|[Gg](2[Gg]|[Tt][Gg]|([Oo]{2,}[Dd]+\s*([Bb]+[Yy]+[Ee]+|[Nn]+[Ii]+[Gg]+[Hh]+[Tt]+)))\s*(!|~|.)*)$')
@priority('high')
def f_bye(bot, trigger):
    set1 = ['bye', 'byebye', 'see you', 'see ya', 'Good bye', 'have a nice day']
    set2 = ['~', '~~~', '!', ' :)', ':D', '(Y)', '(y)', ':P', ':-D', ';)', '(wave)', '(flee)']
    respond = [ str1 + ' ' + str2 for str1 in set1 for str2 in set2]
    bot.say(random.choice(respond))

@rule('^\s*(([Hh]+([AaEe]+[Ll]+[Oo]+|[Ii]+)+\s*(all)?)|[Yy]+[Oo]+|[Aa]+[Ll]+|[Aa]nybody)\s*(!+|\?+|~+|.+|[:;][)DPp]+)*$')
@priority('high')
def f_hello(bot, trigger):
    randtime = random.uniform(0, 7)
    time.sleep(randtime)
    set1 = ['yo', 'hey', 'hi', 'Hi', 'hello', 'Hello', 'Welcome'] # First string options
    set2 = ['~', '~~~', '!', '?', ' :)', ':D', 'xD', '(Y)', '(y)', ':P', ':-D', ';)', ', How do you do?'] # Second string options
    respond = [ str1 + ' ' + str2 for str1 in set1 for str2 in set2] # Pick a string each from set1 and from set 2
    bot.say(random.choice(respond))

@rule('(heh!?)$')
@priority('high')
def f_heh(bot, trigger):
    if decide(bot):
        respond = ['hm', 'hmmmmmm...', 'heh?']
        randtime = random.uniform(0, 7)
        time.sleep(randtime)
        bot.say(random.choice(respond))

@rule('(?i)$nickname\:\s+(really!?)') # Respond to "botnick: really/really?/really!/really!?"
@priority('high')
def f_really(bot, trigger):
    randtime = random.uniform(10, 45) # Time to wait
    time.sleep(randtime) # Wait a bit
    bot.say(str(trigger.nick) + ": " + "Yes, really.") # Respond

@rule('^\s*[Ww]([Bb]|elcome\s*back)[\s:,].*$nickname') # Respond to welcome back botnick/wb botnick
def wb(bot, trigger):
    set1 = ['Thank you', 'thanks'] # First string options
    set2 = ['!', ' :)', ' :D'] # Second string options
    respond = [ str1 + str2 for str1 in set1 for str2 in set2] # Pick a string each from set1 and from set 2
    randtime = random.uniform(0, 7) # Time to wait
    time.sleep(randtime) # Wait a moment
    bot.reply(random.choice(respond)) # Respond

if __name__ == '__main__':
    print(__doc__.strip())

    

### Shared Functions

# Adjust bot config
def set_config(bot, trigger, configentry, value):
    configprefix = "bot.config.ai."
    configkey = configprefix + configentry
    set_success = false
    ### to handle setting config entries
    # if success, set_success = true
    return set_success

# Retrieve bot config
def get_config(bot, trigger, configentry, value):
    configprefix = "bot.config.ai."
    configkey = configprefix + configentry
    config_value = configkey
    return config_value
