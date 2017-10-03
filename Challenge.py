import sopel
from sopel import module, tools
import random
import os
from os.path import exists

script_dir = os.path.dirname(__file__)
rel_path = "data/weapons.txt"
abs_file_path = os.path.join(script_dir, rel_path)

## Enforce challenges. if challenge is not accepted, don't duel
 
#@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
#@module.intent('ACTION')
#def duel_action(bot, trigger):
#    bot.say(trigger.group(1))
#    return duel(bot, trigger.sender, trigger.nick, trigger.group(1), is_admin=trigger.admin, warn_nonexistent=False)

@sopel.module.commands('challenge')
def duel_cmd(bot, trigger):
    return duel(bot, trigger.sender, trigger.nick, trigger.group(3) or '')

def duel(bot, channel, instigator, target, warn_nonexistent=True):
    target = tools.Identifier(target or '')
    weapon = weaponofchoice()
    if not target:
        bot.say(instigator + ", Who did you want to fight?")
    else:
        if target == bot.nick:
            bot.say("I refuse to fight a biological entity!")
        elif target == instigator:
            bot.say("If you want to duel yorself, please find a mirror!")
        elif target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
        else:
            bot.say(instigator + " versus " + target)
            combatants = sorted([instigator, target])
            random.shuffle(combatants)
            winner = combatants.pop()
            loser = combatants.pop()
            bot.say(winner + " wins!")
            bot.say(winner + " killed " + loser + " with " + weapon)

@sopel.module.commands('challengeweapon')
def addweapons(bot, trigger):
    if not trigger.group(3):
        bot.say("what weapon would you like to add?")
    else:
        weaponnew = trigger.group(3)
        with open(abs_file_path, "a") as myfile:
            myfile.write(weaponnew)

def weaponofchoice():
    if exists(abs_file_path):
        try:
            weapons = open(abs_file_path).read().splitlines()
            weapon =random.choice(weapons)
        except IndexError:
            weapons  = ["waffle-iron","fish","knuckle-sandwich","sticky-note","blender","hammer","nailgun","roisserie chicken","steel-toed boot","stapler"]
            weapon = random.randint(0,len(modelnumbers) - 1)
            weapon = str(weapons [weapon])
    else:
        weapon = 'gun'
    if weapon.startswith('a') or weapon.startswith('e') or weapon.startswith('i') or weapon.startswith('o') or weapon.startswith('u'):
        weapon = str('an ' + weapon)
    else:
        weapon = str('a ' + weapon)
    return weapon
