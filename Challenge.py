import sopel
from sopel import module, tools
import random
import os
from os.path import exists
from random import randint

script_dir = os.path.dirname(__file__)
rel_path = "data/weapons.txt"
weaponslocker = os.path.join(script_dir, rel_path)

## Enforce challenges. if challenge is not accepted, don't challenge
## silencer

#@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
#@module.intent('ACTION')
#def challenge_action(bot, trigger):
#    bot.say(trigger.group(1))
#    return challenge(bot, trigger.sender, trigger.nick, trigger.group(1), is_admin=trigger.admin, warn_nonexistent=False)

@sopel.module.commands('challenge')
def challenge_cmd(bot, trigger):
    return challenge(bot, trigger.sender, trigger.nick, trigger.group(3) or '')

def challenge(bot, channel, instigator, target, warn_nonexistent=True):
    target = tools.Identifier(target or '')
    if not target:
        bot.say(instigator + ", Who did you want to fight?")
    else:
        if target == bot.nick:
            bot.say("I refuse to fight a biological entity!")
        elif target == instigator:
            bot.say("If you want to challenge yorself, please find a mirror!")
        elif target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
        else:
            weapon = weaponofchoice()
            damage = damagedone()
            bot.say(instigator + " versus " + target)
            combatants = sorted([instigator, target])
            random.shuffle(combatants)
            winner = combatants.pop()
            loser = combatants.pop()
            bot.say(winner + " wins!")
            update_xp(bot, winner, damage)
            currenthealth = update_health(bot, loser, damage)
            if currenthealth <= 0:
                bot.say(winner + ' killed ' + loser + " with " + weapon + ' forcing a respawn!!')
                respawn(bot, loser)
            else:
                bot.say(winner + " attacks " + loser + " with " + weapon + ', dealing ' + damage + ' damage.')
            
############
## Health ##
############

def get_health(bot, nick):
    health = bot.db.get_nick_value(nick, 'challenges_health') or 1000
    return health

def update_health(bot, nick, damage):
    health = get_health(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_health', health - int(damage))
    currenthealth = get_health(bot, nick)
    return currenthealth

def respawn():
    bot.db.set_nick_value(nick, 'challenges_health', 1000)

def damagedone():
    rando = randint(1, 100)
    if int(rando) >= '75' and int(rando) < '90':
        damage = '5'
    elif int(rando) >= '90':
        damage = '10'
    else:
        damage = '1'
    return damage

########
## XP ##
########

def get_xp(bot, nick):
    xp = bot.db.get_nick_value(nick, 'challenges_xp') or 0
    return xp

def update_xp(bot, nick, damage):
    xp = get_xp(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_xp', xp + int(damage))
    currentxp = get_xp(bot, nick)
    return xp


#############
## Weapons ##
#############

@sopel.module.commands('weaponslocker')
def weaponslockercmd(bot, trigger):
    bot.say('Use weaponslockeradd or weaponslockerdel to adjust Locker Inventory.')

@sopel.module.commands('weaponslockeradd')
def addweapons(bot, trigger):
    checkweapons()
    if not trigger.group(2):
        bot.say("what weapon would you like to add?")
    else:
        weaponnew = str(trigger.group(2))
        if str(weaponnew) in open(weaponslocker).read():
            bot.say(weaponnew + " is already in the weapons locker.")
        else:
            with open(weaponslocker, "a") as myfile:
                myfile.write("\n")
                myfile.write(weaponnew)
            if str(weaponnew) in open(weaponslocker).read():
                bot.say(weaponnew + " has been added to the weapons locker.")

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
@sopel.module.commands('weaponslockerdel')
def removeweapons(bot, trigger):
    checkweapons()
    if not trigger.group(2):
        bot.say("what weapon would you like to remove?")
    else:
        weapondel = str(trigger.group(2))
        if str(weapondel) in open(weaponslocker).read():
            os.system('sudo sed -i "/' + str(weapondel) + '/d; /^$/d" ' + weaponslocker)
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


###########
## Stats ##
###########

@module.commands('challenges')
def duels(bot, trigger):
    target = trigger.group(3) or trigger.nick
    health = get_health(bot, target)
    xp = get_xp(bot, target)
    health = str(target + "'s health is at " + str(health))
    xp = str(target + "'s XP is at " + str(xp))
    bot.say(health + xp)





