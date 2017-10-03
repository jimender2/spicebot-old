import sopel
from sopel import module, tools
import random
import os
from os.path import exists

script_dir = os.path.dirname(__file__)
rel_path = "data/weapons.txt"
weaponslocker = os.path.join(script_dir, rel_path)

## Enforce challenges. if challenge is not accepted, don't duel
## assign XP points
## critical hits

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

@sopel.module.commands('weaponslocker')
def weaponslockercmd(bot, trigger):
    bot.say('Use weaponslockeradd or weaponslockerdel to adjust Locker Inventory.')
            
@sopel.module.commands('weaponslockeradd')
def addweapons(bot, trigger):
    checkweapons()
    if not trigger.group(2):
        bot.say("what weapon would you like to add?")
    else:
        weaponnew = trigger.group(2)
        if str(weaponnew) in open(weaponslocker).read():
            bot.say(weaponnew + " is already in the weapons locker.")
        else:
            with open(weaponslocker, "a") as myfile:
                myfile.write("\n")
                myfile.write(weaponnew)
            if str(weaponnew) in open(weaponslocker).read():
                bot.say(weaponnew + " has been added to the weapons locker.")

@sopel.module.commands('weaponslockerdel')
def removeweapons():
    checkweapons()
    if not trigger.group(2):
        bot.say("what weapon would you like to remove?")
    else:
        weapondel = trigger.group(2)
        if str(weapondel) in open(weaponslocker).read():
            os.system('sudo sed -i "/' + weapondel + '/d ' + weaponslocker)
            if str(weapondel) not in open(weaponslocker).read():
                bot.say(weapondel + ' has been removed from the weapons locker.')
        else:
            bot.say(weapondel + " is not in the weapons locker.")
          
def weaponofchoice():
    checkweapons()
    weapons = open(weaponslocker).read().splitlines()
    weapon =random.choice(weapons)
    if weapon.startswith('a') or weapon.startswith('e') or weapon.startswith('i') or weapon.startswith('o') or weapon.startswith('u'):
        weapon = str('an ' + weapon)
    else:
        weapon = str('a ' + weapon)
    return weapon

def checkweapons():
    if not exists(weaponslocker):
        createweapons()
    if os.stat(weaponslocker).st_size == 0:
        createweapons()
     
def createweapons():
    weapons  = ["waffle-iron","fish","knuckle-sandwich","sticky-note","blender","hammer","nailgun","roisserie chicken","steel-toed boot","stapler"]
    for w in weapons:
        with open(weaponslocker, "a") as myfile:
            if os.stat(weaponslocker).st_size != 0:
                myfile.write("\n")
            myfile.write(w)
