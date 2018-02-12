#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel.module import OP
from sopel.module import ADMIN
from sopel.module import VOICE
import sopel
from sopel import module, tools
import random
from random import randint
import time
import datetime
import re
import sys
import os
from os.path import exists
from num2words import num2words

## not needed if using without spicebot
shareddir = os.path.dirname(os.path.dirname(__file__)) ## not needed if using without spicebot
sys.path.append(shareddir) ## not needed if using without spicebot
from SpicebotShared import * ## not needed if using without spicebot

###################
## Configurables ##
###################

## Command Structure
commandarray_all_valid = ['health','harakiri','tier','bounty','armor','title','docs','admin','author','on','off','usage','stats','loot','streaks','leaderboard','warroom','weaponslocker','class','magic','random','roulette','assault','colosseum']
commandarray_instigator_bypass = ['on','admin'] ## bypass for Opt status
commandarray_channel_activate = ['gameon','gameoff']
commandarray_channel_dev = ['devon','devoff']
commandarray_admin = ['admin'] ## Admin Functions
commandarray_inchannel = ['roulette','assault','colosseum','bounty'] ## Must Be inchannel
### Alternative Commands
commandarray_alt_on = ['enable','activate']
commandarray_alt_off = ['disable','deactivate']
commandarray_alt_random = ['anyone','somebody','available','someone']
commandarray_alt_assault = ['everyone','everybody']
commandarray_alt_author = ['credit']
commandarray_alt_docs = ['help','man']
### Command Tiers
commandarray_tier_self = ['stats', 'loot', 'streaks']
commandarray_tier_unlocks_0 = ['tier', 'docs', 'admin', 'author', 'on', 'off','health'] ## move health to self later
commandarray_tier_unlocks_1 = ['usage']
commandarray_tier_unlocks_2 = ['streaks', 'bounty', 'harakiri']
commandarray_tier_unlocks_3 = ['weaponslocker', 'class']
commandarray_tier_unlocks_4 = ['leaderboard', 'warroom']
commandarray_tier_unlocks_5 = ['stats', 'loot']
commandarray_tier_unlocks_6 = ['magic', 'armor']
commandarray_tier_unlocks_7 = ['assault']
commandarray_tier_unlocks_8 = ['roulette']
commandarray_tier_unlocks_9 = ['random']
commandarray_tier_unlocks_10 = ['colosseum']
commandarray_tier_unlocks_11 = ['title']
commandarray_tier_unlocks_12 = []
commandarray_tier_unlocks_13 = []
commandarray_tier_unlocks_14 = []
commandarray_tier_unlocks_15 = []

## Tiers, XP, Pepper levels
commandarray_xp_levels = [0,1,100,250,500,1000,2500,5000,7500,10000,15000,25000,45000,70000,100000,250000] ## XP
commandarray_tier_ratio = [1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.1,2.2,2.3,2.4,2.5] ## Tier Ratios
commandarray_pepper_levels = ['n00b','pimiento','sonora','anaheim','poblano','jalapeno','serrano','chipotle','tabasco','cayenne','thai pepper','datil','habanero','ghost chili','mace','pure capsaicin'] ## Pepper Levels
commandarray_tier_display_exclude = ['admin'] ## Do NOT display

## more stuff
bodyparts_required = ['torso','head']

## Admin Stats Cycling
stats_admin_types = ['healthbodyparts','armor','loot','record','magic','streak','timeout','class','title','bounty','weaponslocker','leveling']
## Health Stats
# stats_health = ['health_b4se'] ## replace this value throughout
stats_healthbodyparts = ['health_head','health_torso','health_left_arm','health_right_arm','health_left_leg','health_right_leg']
## Armor Stats
stats_armor = ['armor_helmet','armor_breastplate','armor_left_gauntlet','armor_right_gauntlet','armor_left_greave','armor_right_greave']
## Loot Stats
stats_loot = ['loot_magicpotion','loot_healthpotion','loot_mysterypotion','loot_timepotion','loot_poisonpotion','loot_manapotion','loot_grenade','loot_coin']
## Record Stats
stats_record = ['record_wins','record_losses','record_xp','record_respawns','record_kills','record_lastfought']
## Streak Stats
stats_streak = ['streak_loss_current','streak_win_current','streak_type_current','streak_win_best','streak_loss_best']
## Magic Stats
stats_magic = ['magic_mana','magic_curse','magic_shield']
## Timeout Stats
stats_timeout = ['timeout_class','timeout_opttime','timeout_timeout']
## Class Stats
stats_class = ['class_setting','class_freebie','class_timeout']
## Title Stats
stats_title = ['title_setting']
## Bounty Stats
stats_bounty = ['bounty_amount']
## Weaponslocker Stats
stats_weaponslocker = ['weaponslocker_complete','weaponslocker_lastweaponusedarray','weaponslocker_lastweaponused']
## Leveling Stats
stats_leveling = ['leveling_tier']

## Documentation and Development
GITWIKIURL = "https://github.com/deathbybandaid/SpiceBot/wiki/Duels" ## Wiki URL, change if not using with spicebot
development_team = ['deathbybandaid','DoubleD','Mace_Whatdo','dysonparkes','PM','under_score'] ## Dev Team

## On/off
timeout_opt = 1800 ## Time between opting in and out of the game - Half hour

## Roulette
roulette_death_timeout = 86400
timeout_roulette = 5
roulette_payout_default = 5
roulette_revolver_list = ['.357 Magnum','Colt PeaceMaker','Colt Repeater','Colt Single Action Army 45','Ruger Super Blackhawk','Remington Model 1875','Russian Nagant M1895 revolver','Smith and Wesson Model 27']

## Assault
timeout_assault = 1800 ## Time Between Full Channel Assaults
assault_results = ['wins','losses','potionswon','potionslost','kills','deaths','damagetaken','damagedealt','levelups','xp']

## Colosseum
timeout_colosseum = 1800 ## Time Between colosseum events

## Random Target
random_payout = 100

## Class
class_array = ['blacksmith','barbarian','mage','scavenger','rogue','ranger','fiend','vampire','knight','paladin'] ## Valid Classes
timeout_class = 86400 ## Time between changing class - One Day
class_cost = 100 ## ## how many coin to change class

## Title
title_cost = 100 ## ## how many coin to change title

## Bug Bounty
bugbounty_reward = 100 ## users that find a bug in the code, get a reward

## Loot
loot_view = ['loot_coin','loot_grenade','loot_healthpotion','loot_manapotion','loot_poisonpotion','loot_timepotion','loot_mysterypotion','loot_magicpotion'] ## how to organize backpack
potion_types = ['healthpotion','manapotion','poisonpotion','timepotion','mysterypotion','magicpotion'] ## types of potions
loot_transaction_types = ['buy','sell','trade','use'] ## valid commands for loot
### Buy
loot_buy = 100 ## normal cost to buy a loot item
loot_buy_scavenger = 80 ## cost to buy a loot item for scavengers
### Sell
loot_sell = 25 ## normal coin rewarded in selling loot
loot_sell_scavenger = 40 ## coin rewarded in selling loot for scavengers
### Trade
loot_trade = 3 ## normal trading ratio 3:1
loot_trade_scavenger = 2 ## scavengers can trade at a 2:1 ratio
### Grenades
grenade_full_damage = 100
grenade_secondary_damage = 50
### Health Potions
healthpotion_worth = 100 ## normal health potion worth
healthpotion_worth_barbarian = 125 ## health potion worth for barbarians
healthpotiondispmsg = str(": worth " + str(healthpotion_worth) + " health.")
### Mana Potions
manapotion_worth = 100 ##normal mana potion worth
manapotion_worth_mage = 125 ## manapotion worth for mages
manapotiondispmsg = str(": worth " + str(manapotion_worth) + " mana.")
### Poison Potions
poisonpotion_worth = -50 ## poisonpotion damage
poisonpotiondispmsg = str(": worth " + str(poisonpotion_worth) + " health.")
### Mystery Potions
mysterypotiondispmsg = str(": The label fell off. Use at your own risk!")
loot_null = ['water','vinegar','mud']
### Time Potions
timepotiondispmsg = str(": Removes multiple timeouts.")
timepotiontargetarray = ['lastinstigator','lastfullroomcolosseuminstigator','lastfullroomassultinstigator']
timepotiontimeoutarray = ['timeout_timeout','lastfullroomcolosseum','lastfullroomassult','timeout_opttime','class_timeout']
## Magic Potions
magicpotiondispmsg = str(": Not consumable, sellable, or purchasable. Trade this for the potion you want!")

## Weapons Locker
weapon_name_length = 70 ## prevents text that destroys OSD

## Magic
magic_types = ['curse','shield']
magic_usage_mage = .9 ## mages only need 90% of the mana requirements below
magic_mana_required_shield = 300 ## mana required for magic shield
magic_mana_required_curse = 500 ## mana required for magic curse
magic_shield_health = 80 ## health restored by a magic shield usage
magic_shield_duration = 200 ## how long a shield lasts
magic_curse_damage = -80 ## damage caused by a magic curse
magic_curse_duration = 4 ## how long a curse lasts

## Body/Armor
armor_cost = 500
armor_cost_blacksmith_cut = .8 ## TODO
armor_durability = 10
armor_durability_blacksmith = 15
armor_relief_percentage = 33 ## has to be converted to decimal later
health_bodypart_max = [330,1000,250,250,500,500]
## Bodypart damage modifiers

## Half Hour Timer
timeout_auto_opt_out = 259200 ## Opt out users after 3 days of inactivity
halfhour_regen_health, halfhour_regen_health_max = 50,500 ## health regen rate
halfhour_regen_mage_mana, halfhour_regen_mage_mana_max = 50, 500 ## mages regenerate mana: rate
halfhour_coin = 15 ## coin gain per half hour

## Main Duel Runs
duel_lockout_timer = 300
duel_nick_order = ['nicktitles','nickpepper','nickmagicattributes','nickarmor']
duel_hit_types = ['hits','strikes','beats','pummels','bashes','smacks','knocks','bonks','chastises','clashes','clobbers','slugs','socks','swats','thumps','wallops','whops']
bot_damage = 150 ## The bot deals a set damage
USERTIMEOUT = 180 ## Time between a users ability to duel - 3 minutes
CHANTIMEOUT = 40 ## Time between duels in a channel - 40 seconds
INSTIGATORTIMEOUT = 1800 ## Time between instigation, unless another user plays
duel_special_event = 500 ## Every 50 duels, instigator wins 500 coins
### Class (dis)advantages
duel_advantage_scavenger_loot_find = 60 ## scavengers have a higher percent chance of finding loot
duel_advantage_barbarian_min_damage = 60 ## Barbarians always strike a set value or above
duel_disadvantage_vampire_max_damage = 50 ## Vampires have a max damage, but drain that amount from enemy into their own health
duel_advantage_barbarian_rage_chance = 12
duel_advantage_barbarian_rage_max = 25
duel_advantage_paladin_deflect_chance = 12
duel_advantage_knight_retaliate_chance = 12

### XP points awarded
xp_winner = 15 ## default xp earned as a winner
xp_winner_ranger = 20 ## xp earned as a winner and ranger
xp_loser = 10 ## default xp earned as a loser
xp_loser_ranger = 15 ## xp earned as a loser and ranger

## Records
duelrecorduser = 'duelrecorduser'
stat_admin_commands = ['set','reset','view'] ## valid admin subcommands
stats_view = ['class_setting','magic_curse','magic_shield','magic_mana','record_xp','record_wins','record_losses','winlossratio','record_respawns','record_kills','record_lastfought','timeout_timeout','bounty_amount']
stats_view_functions = ['winlossratio','timeout_timeout'] ## stats that use their own functions to get a value


########################
## Main Command Usage ##
########################

## work with /me ACTION (does not work with manual weapon)
@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
@module.intent('ACTION')
@module.require_chanmsg
def duel_action(bot, trigger):
    #triggerargsarray = get_trigger_arg(trigger.group(1), 'create') # enable if not using with spicebot
    #execute_main(bot, trigger, triggerargsarray, 'actionduel') # enable if not using with spicebot
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'duel') ## not needed if using without spicebot
    if not enablestatus: ## not needed if using without spicebot
        execute_main(bot, trigger, triggerargsarray, 'actionduel') ## not needed if using without spicebot

## Base command
@sopel.module.commands('duel','challenge')
def mainfunction(bot, trigger):
    #triggerargsarray = get_trigger_arg(trigger.group(2), 'create') # enable if not using with spicebot
    #execute_main(bot, trigger, triggerargsarray, 'normalcom') # enable if not using with spicebot
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'duel') ## not needed if using without spicebot
    if not enablestatus: ## not needed if using without spicebot
        execute_main(bot, trigger, triggerargsarray, 'normalcom') ## not needed if using without spicebot

####################################
## Seperate Targets from Commands ##
####################################

def execute_main(bot, trigger, triggerargsarray, commandtype):

    ## Instigator
    instigator = trigger.nick

    ## Check command was issued
    fullcommandusedtotal = get_trigger_arg(triggerargsarray, 0)
    commandortarget = get_trigger_arg(triggerargsarray, 1)
    if not fullcommandusedtotal:
        bot.notice(instigator + ", you must specify either a target, or a subcommand. Online Docs: " + GITWIKIURL, instigator)
        return

    ## Game Enabled in what channels
    inchannel = trigger.sender
    if commandortarget.lower() in commandarray_channel_activate:
        if not trigger.admin:
            bot.notice(instigator + ", talk to a bot admin to enable duels in " + inchannel + ".", instigator)
            return
        if not inchannel.startswith("#"):
            bot.notice(instigator + ", duels must be enabled in a channel.", instigator)
            return
        if commandortarget == 'gameon':
            adjust_database_array(bot, duelrecorduser, [inchannel], 'gameenabled', 'add')
            bot.notice(instigator + ", duels  is now on in " + inchannel + ".", instigator)
        else:
            adjust_database_array(bot, duelrecorduser, [inchannel], 'gameenabled', 'del')
            bot.notice(instigator + ", duels  is now off in " + inchannel + ".", instigator)
        return
    gameenabledchannels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
    if gameenabledchannels == []:
        bot.notice(instigator + ", duels has not been enabled in any channels. Talk to a bot admin.", instigator)
        return
    if inchannel not in gameenabledchannels and inchannel.startswith("#"):
        bot.notice(instigator + ", duels has not been enabled in " + inchannel + ". Talk to a bot admin.", instigator)
        return

    ## dev bypass
    if commandortarget.lower() in commandarray_channel_dev:
        if not trigger.admin:
            bot.notice(instigator + ", talk to a bot admin to enable devmode in " + inchannel + ".", instigator)
            return
        if commandortarget == 'devon':
            adjust_database_array(bot, duelrecorduser, [inchannel], 'devenabled', 'add')
            bot.notice(instigator + ", devmode  is now on in " + inchannel + ".", instigator)
        else:
            adjust_database_array(bot, duelrecorduser, [inchannel], 'devenabled', 'del')
            bot.notice(instigator + ", devmode  is now off in " + inchannel + ".", instigator)
        return
    devenabledchannels = get_database_value(bot, duelrecorduser, 'devenabled') or []

    ## user lists
    botvisibleusers = get_database_value(bot, duelrecorduser, 'botvisibleusers') or []
    currentuserlistarray = []
    botvisibleusersappendarray = []
    for user in bot.users:
        if user not in commandarray_all_valid:
            currentuserlistarray.append(user)
            if user not in botvisibleusers:
                botvisibleusersappendarray.append(user)
    adjust_database_array(bot, duelrecorduser, botvisibleusersappendarray, 'botvisibleusers', 'add')
    botvisibleusers = get_database_value(bot, duelrecorduser, 'botvisibleusers') or []

    ## Instigator can't be a command, and can't enable duels
    if instigator.lower() in commandarray_all_valid:
        bot.notice(instigator + ", your nick is the same as a valid command for duels.", instigator)
        return

    ## Instigator can't duelrecorduser
    if instigator.lower() == duelrecorduser:
        bot.notice(instigator + ", your nick is not able to play duels.", instigator)
        return

    ## Check if Instigator is Opted in
    dueloptedinarray = get_database_value(bot, duelrecorduser, 'duelusers') or []
    if instigator not in dueloptedinarray and commandortarget.lower() not in commandarray_instigator_bypass:
        bot.notice(instigator + ", you are not opted into duels. Run `.duel on` to enable duels.", instigator)
        return

    ## Current Duelable Players
    currentduelplayersarray = []
    canduelarray = []
    dowedisplay = 0
    for player in currentuserlistarray:
        if player in dueloptedinarray:
            currentduelplayersarray.append(player)
            executedueling, executeduelingmsg = duelcriteria(bot, instigator, player, currentduelplayersarray, inchannel)
            if executedueling == 1:
                canduelarray.append(player)
                statreset(bot, player) ## TODO
                healthcheck(bot, player) ## TODO

    ## Time when Module use started
    now = time.time()

    ## Instigator last used
    set_database_value(bot, instigator, 'lastcommand', now)

    ## Multiple Commands
    if "&&" not in fullcommandusedtotal:
        commandortargetsplit(bot, trigger, triggerargsarray, instigator, botvisibleusers, currentuserlistarray, dueloptedinarray, now, currentduelplayersarray, canduelarray, commandtype, devenabledchannels)
    else:
        daisychaincount = 0
        fullcomsplit = fullcommandusedtotal.split("&&")
        for comsplit in fullcomsplit:
            ## Freenode kicks bot for excess flood if this is overdone
            daisychaincount = daisychaincount + 1
            if daisychaincount <= 5:
                triggerargsarraypart = get_trigger_arg(comsplit, 'create')
                commandortargetsplit(bot, trigger, triggerargsarraypart, instigator, botvisibleusers, currentuserlistarray, dueloptedinarray, now, currentduelplayersarray, canduelarray, commandtype, devenabledchannels)
            else:
                bot.notice(instigator + ", you may only daisychain 5 commands.", instigator)
                return

def commandortargetsplit(bot, trigger, triggerargsarray, instigator, botvisibleusers, currentuserlistarray, dueloptedinarray, now, currentduelplayersarray, canduelarray, commandtype):

    ## New Vars
    fullcommandused = get_trigger_arg(triggerargsarray, 0)
    commandortarget = get_trigger_arg(triggerargsarray, 1)

    ## Cheap error handling for people that like to find issues
    if commandortarget.isdigit():
        bot.notice(instigator + ", commands can't be numbers.", instigator)
        return

    ## Alternative commands
    for subcom in commandarray_all_valid:
        try:
            commandarray_alt_eval = eval("commandarray_alt_"+subcom)
            if commandortarget.lower() in commandarray_alt_eval:
                commandortarget = subcom
                continue
        except NameError:
            continue

    ## Inchannel Block
    inchannel = trigger.sender
    if commandortarget.lower() in commandarray_inchannel and not inchannel.startswith("#"):
        bot.notice(instigator + ", duel " + commandortarget + " must be in channel.", instigator)
        return

    ## Subcommand Versus Target
    if commandortarget.lower() in commandarray_all_valid:
        ## If command was issued as an action
        if commandtype != 'actionduel':
            subcommands(bot, trigger, triggerargsarray, instigator, fullcommandused, commandortarget, dueloptedinarray, botvisibleusers, now, currentuserlistarray, inchannel, currentduelplayersarray, canduelarray, devenabledchannels)
            return
        else:
            bot.notice(instigator + ", action duels should not be able to run commands. Targets Only", instigator)
            return

    ## Instigator versus Bot
    if commandortarget.lower() == bot.nick.lower():
        bot.say("I refuse to fight a biological entity! If I did, you'd be sure to lose!")
        return

    ## Instigator versus Instigator
    if commandortarget.lower() == instigator.lower():
        bot.say("If you are feeling self-destructive, there are places you can call. Alternatively, you can run the harakiri command")
        return

    ## Targets must be dueled in channel
    if not inchannel.startswith("#"):
        bot.notice(instigator + ", duels must be in channel.", instigator)
        return

    ## Lockout Check, don't allow multiple duels simultaneously
    duelslockout = get_database_value(bot, duelrecorduser, 'duelslockout') or 0
    if duelslockout:
        lockoutsince = get_timesince_duels(bot, instigator, 'duelslockout')
        if lockoutsince < duel_lockout_timer:
            bot.notice(instigator + ", duel(s) is/are currently in progress. You must wait. If this is an error, it should clear itself in 5 minutes.", instigator)
            return
        reset_database_value(bot, duelrecorduser, 'duelslockout')

    ## Check if target is valid
    validtarget, validtargetmsg = targetcheck(bot, commandortarget, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
    if not validtarget:
        bot.notice(validtargetmsg,instigator)
        return

    ## Check that the target doesn't have a timeout preventing them from playing
    executedueling, executeduelingmsg = duelcriteria(bot, instigator, commandortarget, currentduelplayersarray, inchannel)
    if not executedueling:
        bot.notice(executeduelingmsg,instigator)
        return
    
    ## Perform Lockout, run target duel, then unlock
    set_database_value(bot, duelrecorduser, 'duelslockout', now)
    duel_combat(bot, instigator, instigator, [commandortarget], triggerargsarray, now, inchannel, 'target', devenabledchannels)
    reset_database_value(bot, duelrecorduser, 'duelslockout')

    ## usage counter
    adjust_database_value(bot, instigator, 'usage_total', 1)
    adjust_database_value(bot, instigator, 'usage_combat', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_total', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_combat', 1)

#######################
## Subcommands Usage ##
#######################

## Subcommands
def subcommands(bot, trigger, triggerargsarray, instigator, fullcommandused, commandortarget, dueloptedinarray, botvisibleusers, now, currentuserlistarray, inchannel, currentduelplayersarray, canduelarray):

    ## Admin Command Blocker
    if commandortarget.lower() in commandarray_admin and not trigger.admin:
        bot.notice(instigator + ", this admin function is only available to bot admins.", instigator)
        return

    ## Is the Tier Unlocked?
    currenttier = get_database_value(bot, duelrecorduser, 'leveling_tier') or 0
    tiercommandeval = tier_command(bot, commandortarget)
    tierpepperrequired = pepper_tier(bot, tiercommandeval)
    tiermath = int(tiercommandeval) - int(currenttier)
    if int(tiercommandeval) > int(currenttier):
        if commandortarget.lower() not in commandarray_tier_self and not inchannel in devenabledchannels:
            bot.say("Duel " + commandortarget + " will be unlocked when somebody reaches " + str(tierpepperrequired) + ". " + str(tiermath) + " tier(s) remaining!")
            return

    ## usage counter
    adjust_database_value(bot, instigator, 'usage_total', 1)
    adjust_database_value(bot, instigator, 'usage_'+commandortarget.lower(), 1)
    adjust_database_value(bot, duelrecorduser, 'usage_total', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_'+commandortarget.lower(), 1)

    ## If the above passes all above checks
    subcommand_run = str('subcommand_' + commandortarget + '(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels)')
    eval(subcommand_run)

#####################
## Main Duel Usage ##
#####################

def duel_combat(bot, instigator, maindueler, targetarray, triggerargsarray, now, inchannel, typeofduel, devenabledchannels):


    ## Same person can't instigate twice in a row
    set_database_value(bot, duelrecorduser, 'lastinstigator', maindueler)

    ## Starting Tier
    currenttierstart = get_database_value(bot, duelrecorduser, 'leveling_tier') or 0
    tierunlockweaponslocker = tier_command(bot, 'weaponslocker_complete')
    tierscaling = tierratio_level(bot)

    ## Assault Stats
    for astat in assault_results:
        reset_database_value(bot, duelrecorduser, "assault_" + astat)

    ## Targetarray Start
    targetarraytotal = len(targetarray)
    for target in targetarray:
        targetarraytotal = targetarraytotal - 1

        ## target actual
        target = actualname(bot,target)
        
        ## Cleanup from Previous runs
        combattextarraycomplete = []
        texttargetarray = []

        ## Update last fought
        if maindueler != target and typeofduel != 'assault' and typeofduel != 'colosseum':
            set_database_value(bot, maindueler, 'record_lastfought', target)
            set_database_value(bot, target, 'record_lastfought', maindueler)

        ## Assault does not touch lastfought
        if typeofduel == 'assault':
            targetlastfoughtstart = get_database_value(bot, target, 'record_lastfought')

        ## Update Time Of Combat
        set_database_value(bot, maindueler, 'timeout_timeout', now)
        set_database_value(bot, target, 'timeout_timeout', now)
        set_database_value(bot, duelrecorduser, 'timeout_timeout', now)

        ## Display Naming
        mainduelername = duel_names(bot, maindueler, inchannel)
        mainduelerpepperstart = get_pepper(bot, maindueler) ## TODO
        if target == maindueler:
            targetname = "themself"
            targetpepperstart = mainduelerpepperstart
        elif target == bot.nick:
            targetname = target
            targetpepperstart = get_pepper(bot, target)
        else:
            targetname = duel_names(bot, target, inchannel)
            targetpepperstart = get_pepper(bot, target)

        ## Announce Combat
        combattextarraycomplete.append(mainduelername + " versus " + targetname)

        ## Chance of maindueler finding loot
        if target != bot.nick and maindueler != target:
            randominventoryfind = randominventory(bot, maindueler)
            if randominventoryfind == 'true':
                loot = get_trigger_arg(potion_types, 'random')
                loot_text = eval(loot+"dispmsg")
                combattextarraycomplete.append(maindueler + ' found a ' + str(loot) + ' ' + str(loot_text))

        ## Select winner Based on Stats
        if target == bot.nick:
            winner = bot.nick
            loser = mainduelername
            losername = targetname
        elif target == maindueler:
            winner = maindueler
            loser = maindueler
            losername = targetname
        else:
            winner = selectwinner(bot, [maindueler, target])
            if winner == maindueler:
                loser = target
                losername = targetname
            else:
                loser = maindueler
                losername = mainduelername
        if winner == maindueler:
            adjust_database_value(bot, duelrecorduser, 'assault_wins', 1)
        else:
            adjust_database_value(bot, duelrecorduser, 'assault_losses', 1)

        ## Classes
        classwinner = get_database_value(bot, winner, 'class_setting') or 'notclassy'
        classloser = get_database_value(bot, loser, 'class_setting') or 'notclassy'

        ## Current Streaks
        winner_loss_streak, loser_win_streak = get_current_streaks(bot, winner, loser)

        ## Update Wins and Losses
        if maindueler != target:
            adjust_database_value(bot, winner, 'record_wins', 1)
            adjust_database_value(bot, loser, 'record_losses', 1)
            set_current_streaks(bot, winner, 'win')
            set_current_streaks(bot, loser, 'loss')

        ## Manual weapon
        weapon = get_trigger_arg(triggerargsarray, '2+')
        if winner == maindueler and weapon and currenttierstart >= tierunlockweaponslocker:
            if weapon == 'all':
                weapon = getallchanweaponsrandom(bot)
            elif weapon == 'target':
                weapon = weaponofchoice(bot, target)
                weapon = str(target + "'s " + weapon)
        elif winner == bot.nick:
            weapon = ''
        else:
            weapon = weaponofchoice(bot, winner)
        weapon = weaponformatter(bot, weapon)
        if weapon != '':
            weapon = str(" " + weapon)

        ## Magic Attributes Start
        winnershieldstart, winnercursestart = get_current_magic_attributes(bot, winner)
        losershieldstart, losercursestart = get_current_magic_attributes(bot, loser)

        ## Body Part Hit
        currentbodypartsarray = bodypartarray(bot, loser)
        bodypart = get_trigger_arg(currentbodypartsarray, 'random')
        bodypartname = bodypart.split("_", 1)[1]
        bodypartname = bodypartname.replace("_", " ")

        ## Strike Type
        striketype = get_trigger_arg(duel_hit_types, 'random')

        ## Damage
        damage = duels_damage(bot, tierscaling, classwinner, classloser, winner, loser)
        damage = int(damage)

        ## Damage Text
        roguearray = [bot.nick]
        if winner == loser:
            roguearray.append(winner)
        if classloser == 'rogue' and winner in roguearray:
            damagetext = str(loser + " takes no damage in this encounter")
        else:
            damagetext = duels_damage_text(bot, damage, winner, loser, bodypart, striketype, weapon, classwinner, bodypartname, winner, loser)
        combattextarraycomplete.append(damagetext)

        ## Vampires gain health from wins
        if classwinner == 'vampire' and winner != loser:
            splitdamage = int(damage) / 6
            for part in stats_healthbodyparts:
                adjust_database_value(bot, winner, part, splitdamage)

        ## Berserker Rage
        if classwinner == 'barbarian' and winner != loser:
            rageodds = randint(1, duel_advantage_barbarian_rage_chance)
            if rageodds == 1:
                extradamage = randint(1, duel_advantage_barbarian_rage_max)
                combattextarraycomplete.append(winner + " goes into Berserker Rage for an extra " + str(extradamage) + " damage.")
                extradamage = extradamage * tierscaling
                damage = damage + extradamage

        ## Paladin deflect
        persontotakedamage = loser
        if classloser == 'paladin' and damage > 0 and winner != loser:
            deflectodds = randint(1, duel_advantage_paladin_deflect_chance)
            if deflectodds == 1:
                persontotakedamage = winner
                combattextarraycomplete.append(loser + " deflects the damage back on " + winner + ". ")
                damage, damagetextarray = damage_resistance(bot, winner, damage, bodypart)
                for x in damagetextarray:
                    combattextarraycomplete.append(x)
                if damage > 0:
                    if winner == maindueler:
                        adjust_database_value(bot, duelrecorduser, 'assault_damagetaken', damage)
                    else:
                        adjust_database_value(bot, duelrecorduser, 'assault_damagedealt', damage)
                    adjust_database_value(bot, loser, bodypart, -abs(damage))
                    ## Update Health Of winner, respawn, allow loser to loot
                    winnerheadhealth = get_database_value(bot, winner, 'health_head')
                    winnertorsohealth = get_database_value(bot, winner, 'health_torso')
                    if winnerheadhealth  <= 0 or winnertorsohealth <= 0:
                        if winner == maindueler:
                            adjust_database_value(bot, duelrecorduser, 'assault_deaths', 1)
                        else:
                            adjust_database_value(bot, duelrecorduser, 'assault_kills', 1)
                        loserkilledwinner = whokilledwhom(bot, loser, winner) or ''
                        for x in loserkilledwinner:
                            combattextarraycomplete.append(x)
                    else:
                        winnercurrenthealthbody  = get_database_value(bot, winner, bodypart)
                        if winnercurrenthealthbody  <= 0:
                            combattextarraycomplete.append(winner + "'s " + bodypartname + " has become crippled!")
                damage = 0

        ## Damage Resist
        if damage > 0:
            damage, damagetextarray = damage_resistance(bot, loser, damage, bodypart)
            for x in damagetextarray:
                combattextarraycomplete.append(x)
            if damage > 0:
                if winner == maindueler:
                    adjust_database_value(bot, duelrecorduser, 'assault_damagedealt', damage)
                else:
                    adjust_database_value(bot, duelrecorduser, 'assault_damagetaken', damage)
                adjust_database_value(bot, loser, bodypart, -abs(damage))
                ## Update Health Of loser, respawn, allow winner to loot
                loserheadhealth = get_database_value(bot, loser, 'health_head')
                losertorsohealth = get_database_value(bot, loser, 'health_torso')
                if loserheadhealth  <= 0 or losertorsohealth <= 0:
                    if winner == maindueler:
                        adjust_database_value(bot, duelrecorduser, 'assault_kills', 1)
                    else:
                        adjust_database_value(bot, duelrecorduser, 'assault_deaths', 1)
                    winnerkilledloser = whokilledwhom(bot, winner, loser) or ''
                    for x in winnerkilledloser:
                        combattextarraycomplete.append(x)
                else:
                    losercurrenthealthbody  = get_database_value(bot, loser, bodypart)
                    if losercurrenthealthbody  <= 0:
                        combattextarraycomplete.append(loser + "'s " + bodypartname + " has become crippled!")

        ## Knight Retaliation
        if classloser == 'knight' and winner != loser:
            retaliateodds = randint(1, duel_advantage_knight_retaliate_chance)
            if retaliateodds == 1:
                ## Weapon
                weaponb = weaponofchoice(bot, loser)
                weaponb = weaponformatter(bot, weaponb)
                weaponb = str(" "+ weaponb)
                ## Body Part Hit
                currentbodypartsarrayb = bodypartarray(bot, winner)
                bodypartb = get_trigger_arg(currentbodypartsarrayb, 'random')
                bodypartnameb = bodypartb.split("_", 1)[1]
                bodypartnameb = bodypartnameb.replace("_", " ")
                ## Strike Type
                striketypeb = get_trigger_arg(duel_hit_types, 'random')
                ## Damage
                damageb = duels_damage(bot, tierscaling, classloser, classwinner, loser, winner)
                damagetextb = duels_damage_text(bot, damage, loser, winner, bodypartb, striketypeb, weaponb, classloser, bodypartnameb, loser, winner)
                combattextarraycomplete.append(damagetextb)
                ## Damage Resist
                if damage > 0:
                    damage, damagetextarray = damage_resistance(bot, loser, damage, bodypart)
                    for x in damagetextarray:
                        combattextarraycomplete.append(x)
                    if damage > 0:
                        if winner == maindueler:
                            adjust_database_value(bot, duelrecorduser, 'assault_damagetaken', damage)
                        else:
                            adjust_database_value(bot, duelrecorduser, 'assault_damagedealt', damage)
                        adjust_database_value(bot, winner, bodypartb, -abs(damage))
                        ## Update Health Of winner, respawn, allow loser to loot
                        winnerheadhealth = get_database_value(bot, winner, 'health_head')
                        winnertorsohealth = get_database_value(bot, winner, 'health_torso')
                        if winnerheadhealth  <= 0 or winnertorsohealth <= 0:
                            if winner == maindueler:
                                adjust_database_value(bot, duelrecorduser, 'assault_deaths', 1)
                            else:
                                adjust_database_value(bot, duelrecorduser, 'assault_kills', 1)
                            loserkilledwinner = whokilledwhom(bot, loser, winner) or ''
                            for x in loserkilledwinner:
                                combattextarraycomplete.append(x)
                        else:
                            winnercurrenthealthbody  = get_database_value(bot, winner, bodypart)
                            if winnercurrenthealthbody  <= 0:
                                combattextarraycomplete.append(winner + "'s " + bodypartnameb + " has become crippled!")

        ## Chance that maindueler loses found loot
        if target != bot.nick and maindueler != target:
            if randominventoryfind == 'true':
                ## Barbarians get a 50/50 chance of getting loot even if they lose
                classloser = get_database_value(bot, loser, 'class_setting') or 'notclassy'
                barbarianstealroll = randint(0, 100)
                if classloser == 'barbarian' and barbarianstealroll >= 50:
                    combattextarraycomplete.append(loser + " steals the " + str(loot))
                    lootwinner = loser
                elif winner == target:
                    combattextarraycomplete.append(winner + " gains the " + str(loot))
                    lootwinner = winner
                else:
                    lootwinner = winner
                adjust_database_value(bot, lootwinner, "loot_"+loot, 1)
                if lootwinner == maindueler:
                    adjust_database_value(bot, duelrecorduser, 'assault_potionswon', 1)
                else:
                    adjust_database_value(bot, duelrecorduser, 'assault_potionslost', 1)

        ## Update XP points
        if classwinner == 'ranger':
            XPearnedwinner = xp_winner_ranger
        else:
            XPearnedwinner = xp_winner
        if classloser == 'ranger':
            XPearnedloser = xp_loser_ranger
        else:
            XPearnedloser = xp_loser
        if maindueler != target and target != bot.nick:
            winnertier = get_database_value(bot, winner, 'leveling_tier')
            losertier = get_database_value(bot, loser, 'leveling_tier')
            if winnertier < currenttierstart:
                XPearnedwinner = XPearnedwinner * tierscaling
            if losertier < currenttierstart:
                XPearnedloser = XPearnedloser * tierscaling
            adjust_database_value(bot, winner, 'record_xp', XPearnedwinner)
            adjust_database_value(bot, loser, 'record_xp', XPearnedloser)
            if winner == maindueler:
                adjust_database_value(bot, duelrecorduser, 'assault_xp', XPearnedwinner)
            else:
                adjust_database_value(bot, duelrecorduser, 'assault_xp', XPearnedloser)

        ## new pepper level?
        mainduelerpeppernow = get_pepper(bot, maindueler)
        if mainduelerpeppernow != mainduelerpepperstart and maindueler != target:
            combattextarraycomplete.append(maindueler + " graduates to " + mainduelerpeppernow + "! ")
            adjust_database_value(bot, duelrecorduser, 'assault_levelups', 1)
        targetpeppernow = get_pepper(bot, target)
        if targetpeppernow != targetpepperstart and maindueler != target and target != bot.nick:
            combattextarraycomplete.append(target + " graduates to " + targetpeppernow + "! ")

        ## Tier update
        currenttierend = get_database_value(bot, duelrecorduser, 'leveling_tier') or 1
        if int(currenttierend) > int(currenttierstart):
            combattextarraycomplete.append("New Tier Unlocked!")
            tiercheck = eval("commandarray_tier_unlocks_"+str(currenttierend))
            if tiercheck != []:
                newtierlist = get_trigger_arg(tiercheck, "list")
                combattextarraycomplete.append("Feature(s) now available: " + newtierlist)

        ## Magic Attributes text
        if maindueler != target:
            magicattributestext = get_magic_attributes_text(bot, winner, loser, winnershieldstart, losershieldstart, winnercursestart , losercursestart)
            for x in magicattributestext:
                combattextarraycomplete.append(x)

        ## Special Event
        speceventtext = ''
        speceventtotal = get_database_value(bot, duelrecorduser, 'specevent') or 0
        if speceventtotal >= 49:
            set_database_value(bot, duelrecorduser, 'specevent', 1)
            combattextarraycomplete.append(maindueler + " triggered the special event! Winnings are "+str(duel_special_event)+" Coins!")
            adjust_database_value(bot, maindueler, 'loot_coin', duel_special_event)
        else:
            adjust_database_value(bot, duelrecorduser, 'specevent', 1)

        ## Streaks Text
        if maindueler != target:
            streaktext = get_streaktext(bot, winner, loser, winner_loss_streak, loser_win_streak) or ''
            if streaktext != '':
                combattextarraycomplete.append(streaktext)

        ## Random Bonus
        if typeofduel == 'random' and winner == maindueler:
            adjust_database_value(bot, winner, 'loot_coin', random_payout)
            combattextarraycomplete.append(maindueler + " won the random attack payout!")

        ## On Screen Text
        if typeofduel != 'assault' and typeofduel != 'colosseum':
            onscreentext(bot, [inchannel], combattextarraycomplete)
        else:
            onscreentext(bot, [winner,loser], combattextarraycomplete)

        ## Pause Between duels
        if typeofduel == 'assault':
            bot.notice("  ", maindueler)
            time.sleep(5)

        ## End Of assault
        if typeofduel == 'assault':
            set_database_value(bot, target, 'record_lastfought', targetlastfoughtstart)
            if targetarraytotal == 0:
                bot.notice(maindueler + ", It looks like the Full Channel Assault has completed.", maindueler)
                assaultstatsarray = []
                assaultstatsarray.append(maindueler + "'s Full Channel Assault results:")
                for astat in assault_results:
                    astateval = get_database_value(bot, duelrecorduser, "assault_" + astat) or 0
                    if astateval:
                        astatstr = str(str(astat) + " = " + str(astateval))
                        assaultstatsarray.append(astatstr)
                        reset_database_value(bot, duelrecorduser, "assault_" + astat)
                onscreentext(bot, [inchannel], assaultstatsarray)

#################
## Subcommands ##
#################

## Author Subcommand
def subcommand_author(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    bot.say("The author of Duels is deathbybandaid.")

## Docs Subcommand
def subcommand_docs(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    target = get_trigger_arg(triggerargsarray, 2)
    if not target:
        bot.say("Online Docs: " + GITWIKIURL)
        return
    ## private message player
    validtarget, validtargetmsg = targetcheck(bot, commandortarget, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
    if not validtarget:
        bot.notice(validtargetmsg, instigator)
        return
    bot.notice("Online Docs: " + GITWIKIURL, target)

## On Subcommand
def subcommand_on(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):

    ## User can't toggle status all the time
    instigatoropttime = get_timesince_duels(bot, instigator, 'timeout_opttime')
    if instigatoropttime < timeout_opt and not inchannel in devenabledchannels:
        bot.notice(instigator + " It looks like you can't enable/disable duels for " + str(hours_minutes_seconds((timeout_opt - instigatoropttime))), instigator)
        return

    ## check if player already has duels on
    if instigator.lower() in [x.lower() for x in dueloptedinarray]:
        bot.notice(instigator + ", It looks like you already have duels on.", instigator)
        return

    ## make the adjustment
    adjust_database_array(bot, duelrecorduser, [instigator], 'duelusers', 'add')
    set_database_value(bot, instigator, 'timeout_opttime', now)
    bot.notice(instigator + ", duels should now be " +  commandortarget + " for you.", instigator)

    ## Anounce to channels
    gameenabledchannels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
    dispmsgarray = []
    dispmsgarray.append(instigator + " has entered the arena!")
    onscreentext(bot, gameenabledchannels, dispmsgarray)

## Off Subcommand
def subcommand_off(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):

    ## User can't toggle status all the time
    instigatoropttime = get_timesince_duels(bot, instigator, 'timeout_opttime')
    if instigatoropttime < timeout_opt and not inchannel in devenabledchannels:
        bot.notice(instigator + " It looks like you can't enable/disable duels for " + str(hours_minutes_seconds((timeout_opt - instigatoropttime))), instigator)
        return

    ## check if player already has duels off
    if instigator.lower() not in [x.lower() for x in dueloptedinarray]:
        bot.notice(instigator + ", It looks like you already have duels off.", instigator)
        return

    ## make the adjustment
    adjust_database_array(bot, duelrecorduser, [instigator], 'duelusers', 'del')
    set_database_value(bot, instigator, 'timeout_opttime', now)
    bot.notice(instigator + ", duels should now be " +  commandortarget + " for you.", instigator)

    ## Anounce to channels
    gameenabledchannels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
    dispmsgarray = []
    dispmsgarray.append(instigator + " has left the arena! What a coward!")
    onscreentext(bot, gameenabledchannels, dispmsgarray)

## Health Subcommand
def subcommand_health(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    healthcommand = get_trigger_arg(triggerargsarray, 2) or instigator
    if not healthcommand or healthcommand.lower() in [x.lower() for x in dueloptedinarray]:
        if int(tiercommandeval) > int(currenttier) and healthcommand != instigator:
            bot.notice(instigator + ", health for other players cannot be viewed until somebody reaches " + str(tierpepperrequired.title()) + ". "+str(tiermath) + " tier(s) remaining!", instigator)
            if not inchannel in devenabledchannels:
                return
        validtarget, validtargetmsg = targetcheck(bot, healthcommand, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
        if not validtarget:
            bot.notice(validtargetmsg, instigator)
            return
        healthcommand = actualname(bot, healthcommand)
        dispmsgarray = []
        totalhealth = 0
        for x in stats_healthbodyparts:
            gethowmany = get_database_value(bot, healthcommand, x)
            if gethowmany:
                xname = x.split("_", 1)[1]
                xname = xname.replace("_", " ")
                xname = xname.title()
                dispmsgarray.append(str(xname) + "=" + str(gethowmany))
                totalhealth = totalhealth + gethowmany
        dispmsgarrayb = []
        if dispmsgarray != []:
            dispmsgarrayb.append(healthcommand + "'s " + commandortarget + ":")
            dispmsgarrayb.append("Total Health=" + str(totalhealth))
            for y in dispmsgarray:
                dispmsgarrayb.append(y)
        else:
            dispmsgarrayb.append(instigator + ", It looks like " + healthcommand + " has no " +  commandortarget + ".")
        onscreentext(bot, ['say'], dispmsgarrayb)

## Tier Subcommand
def subcommand_tier(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    command = get_trigger_arg(triggerargsarray, 2)
    dispmsgarray = []
    currenttierpepper = pepper_tier(bot, currenttier)
    dispmsgarray.append("The current tier is " + str(currenttier)+ " ("+ str(currenttierpepper.title()) + ").")

    ## Display current/future features
    if not command:
        currenttierlistarray = []
        futuretierlistarray = []
        for i in range(0,16):
            tiercheck = eval("commandarray_tier_unlocks_"+str(i))
            for x in tiercheck:
                if i <= currenttier:
                    if x not in commandarray_tier_display_exclude:
                        currenttierlistarray.append(x)
                else:
                    if x not in commandarray_tier_display_exclude:
                        futuretierlistarray.append(x)
        if currenttierlistarray != []:
            currenttierlist = get_trigger_arg(currenttierlistarray, "list")
            dispmsgarray.append("Feature(s) currently available: " + currenttierlist + ".")
        if futuretierlistarray != []:
            futuretierlist = get_trigger_arg(futuretierlistarray, "list")
            dispmsgarray.append("Feature(s) not yet unlocked: " + futuretierlist + ".")

    ## Don't show list
    elif command.lower() in commandarray_tier_display_exclude:
        bot.notice(instigator + ", that appears to be an invalid command.", instigator)
        return

    ## What tier is next
    elif command.lower() == 'next':
        nexttier = currenttier + 1
        if nexttier > 15:
            bot.say("Tiers do not got past 15 (Pure Capsaicin).")
            return
        nextpepper = pepper_tier(bot, nexttier)
        tiercheck = eval("commandarray_tier_unlocks_"+str(nexttier))
        if tiercheck != []:
            tierlist = get_trigger_arg(tiercheck, "list")
            dispmsgarray.append("Feature(s) that are available at tier " + str(nexttier) + " (" + str(nextpepper.title()) +"): " + tierlist + ".")
        else:
            dispmsgarray.append("No New Feature(s) available at tier " + str(nexttier) + " (" + str(nextpepper.title()) + ").")

    ## Find what tier a command is in
    elif command.lower() in commandarray_all_valid:
        commandtier = tier_command(bot, command)
        commandpepper = pepper_tier(bot, commandtier)
        dispmsgarray.append("The " + str(command) + " is unlocked at tier " + str(commandtier)+ " ("+ str(commandpepper.title()) + ").")
        tiercheck = eval("commandarray_tier_unlocks_"+str(commandtier))
        tiermath = commandtier - currenttier
        if tiermath > 0:
            dispmsgarray.append(str(tiermath) + " tier(s) remaining!")

    ## find what tier a pepper level is
    elif command.lower() in commandarray_pepper_levels:
        commandtier = tier_pepper(bot, command)
        tiercheck = eval("commandarray_tier_unlocks_"+str(commandtier))
        if tiercheck != []:
            tierlist = get_trigger_arg(tiercheck, "list")
            dispmsgarray.append("Feature(s) that are available at tier " + str(commandtier) + " (" + str(command.title()) +"): " + tierlist + ".")
        else:
            dispmsgarray.append("No New Feature(s) available at tier " + str(commandtier) + " (" + str(command.title()) + ").")
        tiermath = int(commandtier) - currenttier
        if tiermath > 0:
            dispmsgarray.append(str(tiermath) + " tier(s) remaining!")

    ## process a tier number
    elif command.isdigit():
        command = int(command)
        if int(command) > 15:
            bot.say("Tiers do not got past 15 (Pure Capsaicin).")
            return
        commandpepper = pepper_tier(bot, command)
        tiercheck = eval("commandarray_tier_unlocks_"+str(command))
        if tiercheck != []:
            tierlist = get_trigger_arg(tiercheck, "list")
            dispmsgarray.append("Feature(s) that are available at tier " + str(command) + " (" + str(commandpepper.title()) +"): " + tierlist + ".")
        else:
            dispmsgarray.append("No New Feature(s) available at tier " + str(command) + " (" + str(commandpepper.title()) + ").")
        tiermath = int(command) - currenttier
        if tiermath > 0:
            dispmsgarray.append(str(tiermath) + " tier(s) remaining!")

    ## find the player with the most xp, and how long until they reach a new tier
    elif command.lower() == 'closest':
        statleadername = ''
        statleadernumber  = 0
        for user in currentuserlistarray:
            statamount = get_database_value(bot, user, 'record_xp')
            if statamount >= statleadernumber and statamount > 0:
                statleadername = user
                statleadernumber = statamount
        if statleadername != '':
            nexttier = currenttier + 1
            if int(nexttier) > 15:
                bot.say("Tiers do not got past 15 (Pure Capsaicin).")
                return
            tierxprequired = get_trigger_arg(commandarray_xp_levels, nexttier)
            tierxpmath = tierxprequired - statleadernumber
            dispmsgarray.append("The leader in xp is " + statleadername + " with " + str(statleadernumber) + ". The next tier is " + str(abs(tierxpmath)) + " xp away.")
            nextpepper = pepper_tier(bot, nexttier)
            tiercheck = eval("commandarray_tier_unlocks_"+str(nexttier))
            if tiercheck != []:
                tierlist = get_trigger_arg(tiercheck, "list")
                dispmsgarray.append("Feature(s) that are available at tier " + str(nexttier) + " (" + str(nextpepper.title()) +"): " + tierlist + ".")
            else:
                dispmsgarray.append("No New Feature(s) available at tier " + str(nexttier) + " (" + str(nextpepper.title()) + ").")
            tiermath = int(nexttier) - currenttier
            if tiermath > 0:
                dispmsgarray.append(str(tiermath) + " tier(s) remaining!")
        else:
            dispmsgarray.append("Nobody is the closest to the next pepper level.")

    ## anything else is deemed a target, see what tier they are on if valid
    else:
        validtarget, validtargetmsg = targetcheck(bot, command, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
        if not validtarget:
            bot.notice(validtargetmsg, instigator)
            return
        targettier = get_database_value(bot, command, 'leveling_tier') or 0
        dispmsgarray.append(command + "'s current tier is " + str(targettier)+ ". ")

    ## display the info
    onscreentext(bot, ['say'], dispmsgarray)

## Suicide/harakiri
def subcommand_harakiri(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    target = get_trigger_arg(triggerargsarray, 2) or instigator
    if target != instigator and target != 'confirm':
        bot.say("You can't suicide other people. It's called Murder.")
    elif target == instigator:
        bot.say("You must run this command with 'confirm' to kill yourself. No rewards are given in to cowards.")
    else:
        suicidetextarray = suicidekill(bot,instigator)
        onscreentext(bot, ['say'], suicidetextarray)

## Russian Roulette
def subcommand_roulette(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):

    ## instigator must wait until the next round
    roulettelastshot = get_database_value(bot, duelrecorduser, 'roulettelastplayershot') or bot.nick
    if roulettelastshot == instigator and not inchannel in devenabledchannels:
        bot.notice(instigator + ", you must wait for the current round to complete, until you may play again.", instigator)
        return

    ## Instigator must wait a day after death
    getlastdeath = get_timesince_duels(bot, instigator, 'roulettedeath') or roulette_death_timeout
    if getlastdeath < roulette_death_timeout and not inchannel in devenabledchannels:
        bot.notice(instigator + ", you must wait 24 hours between roulette deaths.", instigator)
        return

    ## Small timeout
    getlastusage = get_timesince_duels(bot, duelrecorduser, str('lastfullroom' + commandortarget)) or timeout_roulette
    if getlastusage < timeout_roulette and not inchannel in devenabledchannels:
        bot.notice(instigator + " Roulette has a small timeout.", instigator)
        return
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget), now)

    ## Check who last pulled the trigger, or if it's a new chamber
    roulettelastplayer = get_database_value(bot, duelrecorduser, 'roulettelastplayer') or bot.nick
    roulettecount = get_database_value(bot, duelrecorduser, 'roulettecount') or 1

    ## Get the selected chamber from the database,, or set one
    roulettechamber = get_database_value(bot, duelrecorduser, 'roulettechamber')
    if not roulettechamber:
        roulettechamber = randint(1, 6)
        set_database_value(bot, duelrecorduser, 'roulettechamber', roulettechamber)

    ## Display Text
    instigatorcurse = get_database_value(bot, instigator, 'magic_curse') or 0
    if instigatorcurse:
        bot.say(instigator + " spins the cylinder to the bullet's chamber and pulls the trigger.")
    elif roulettelastplayer == instigator and int(roulettecount) > 1:
        bot.say(instigator + " spins the revolver and pulls the trigger.")
    elif int(roulettecount) == 1:
        bot.say(instigator + " reloads the revolver, spins the cylinder and pulls the trigger.")
    else:
        bot.say(instigator + " spins the cylinder and pulls the trigger.")

    ## Default 6 possible locations for bullet.
    ### curses
    if instigatorcurse:
        adjust_database_value(bot, instigator, 'magic_curse', -1)
        reset_database_value(bot, duelrecorduser, 'roulettespinarray')
        currentspin = roulettechamber
    ### If instigator uses multiple times in a row, decrease odds of success
    elif roulettelastplayer == instigator:
        roulettespinarray = get_database_value(bot, duelrecorduser, 'roulettespinarray')
        if not roulettespinarray:
            roulettespinarray = [1,2,3,4,5,6]
        if len(roulettespinarray) > 1:
            roulettetemp = []
            for x in roulettespinarray:
                if int(x) != int(roulettechamber):
                    roulettetemp.append(x)
            rouletteremove = get_trigger_arg(roulettetemp, "random")
            roulettetempb = []
            roulettetempb.append(roulettechamber)
            for j in roulettetemp:
                if int(j) != int(rouletteremove):
                    roulettetempb.append(j)
            set_database_value(bot, duelrecorduser, 'roulettespinarray', roulettetempb)
            currentspin = get_trigger_arg(roulettetempb, "random")
        else:
            currentspin = roulettechamber ## if only one location left
            reset_database_value(bot, duelrecorduser, 'roulettespinarray')
    else:
        roulettespinarray = [1,2,3,4,5,6]
        reset_database_value(bot, duelrecorduser, 'roulettespinarray')
        currentspin = get_trigger_arg(roulettespinarray, "random")

    ### current spin is safe
    if int(currentspin) != int(roulettechamber):
        time.sleep(2) # added to build suspense
        bot.say("*click*")
        roulettecount = roulettecount + 1
        roulettepayout = roulette_payout_default * roulettecount
        adjust_database_value(bot, instigator, 'roulettepayout', roulettepayout)
        set_database_value(bot, duelrecorduser, 'roulettecount', roulettecount)
        set_database_value(bot, duelrecorduser, 'roulettelastplayer', instigator)
        adjust_database_array(bot, duelrecorduser, [instigator], 'roulettewinners', 'add')

    ### instigator shoots themself in the head
    else:
        dispmsgarray = []
        if roulettecount == 1:
            if instigatorcurse:
                dispmsgarray.append("First in the chamber. Looks like " + instigator + " was cursed!")
            else:
                dispmsgarray.append("First in the chamber. What bad luck.")

        ## Dish out the pain
        damage = randint(50, 120)
        bodypart = 'head'
        revolver = get_trigger_arg(roulette_revolver_list, 'random')
        damagescale = tierratio_level(bot)
        damage = damagescale * damage
        dispmsgarray.append(instigator + " shoots themself in the head with the " + revolver + ", dealing " + str(damage) + " damage. ")
        damage, damagetextarray = damage_resistance(bot, instigator, damage, bodypart)
        for x in damagetextarray:
            dispmsgarray.append(x)
        if damage > 0:
            adjust_database_value(bot, instigator, 'health_head', -abs(damage))
            instigatorcurrenthealth  = get_database_value(bot, instigator, 'health_head')
            if instigatorcurrenthealth  <= 0:
                suicidetextarray = suicidekill(bot,instigator)
                for x in suicidetextarray:
                    dispmsgarray.append(x)

        ## Payouts
        biggestpayout, biggestpayoutwinner = 0,''
        roulettewinners = get_database_value(bot, duelrecorduser, 'roulettewinners') or []
        uniquewinnersarray = []
        for x in roulettewinners:
            if x not in uniquewinnersarray and x != instigator:
                uniquewinnersarray.append(x)
        for x in uniquewinnersarray:
            roulettepayoutx = get_database_value(bot, x, 'roulettepayout')
            if roulettepayoutx > biggestpayout:
                biggestpayoutwinner = x
                biggestpayout = roulettepayoutx
            elif roulettepayoutx == biggestpayout:
                biggestpayoutwinner = str(biggestpayoutwinner+ " " + x)
                biggestpayout = roulettepayoutx
            adjust_database_value(bot, x, 'loot_coin', roulettepayoutx)
            bot.notice(x + ", your roulette payouts = " + str(roulettepayoutx) + " coins!", x)
            reset_database_value(bot, x, 'roulettepayout')
        if uniquewinnersarray != []:
            displaymessage = get_trigger_arg(uniquewinnersarray, "list")
            if len(uniquewinnersarray) > 1:
                dispmsgarray.append("Winners: " + displaymessage + ".")
            else:
                dispmsgarray.append("Winner: " + displaymessage + ".")
        if biggestpayoutwinner != '':
            dispmsgarray.append("Biggest Payout: "+ biggestpayoutwinner + " with " + str(biggestpayout) + " coins.")
        roulettecount = get_database_value(bot, duelrecorduser, 'roulettecount') or 1
        if roulettecount > 1:
            roulettecount = roulettecount + 1
            dispmsgarray.append("The chamber spun " + str(roulettecount) + " times. ")
        onscreentext(bot, [inchannel], dispmsgarray)

        ## instigator must wait until the next round
        reset_database_value(bot, duelrecorduser, 'roulettelastplayershot')
        set_database_value(bot, duelrecorduser, 'roulettelastplayershot', instigator)

        ### Reset for next run
        reset_database_value(bot, duelrecorduser, 'roulettelastplayer')
        reset_database_value(bot, duelrecorduser, 'roulettechamber')
        reset_database_value(bot, duelrecorduser, 'roulettewinners')
        reset_database_value(bot, duelrecorduser, 'roulettecount')
        reset_database_value(bot, instigator, 'roulettepayout')

## Colosseum/hungergames
def subcommand_colosseum(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    ## TODO tie this in with duel_combat
    ### go through the target array for instigator
    ### change instigator throughout that function for lastfought purposes
    if bot.nick in canduelarray:
        canduelarray.remove(bot.nick)
    executedueling, executeduelingmsg = eventchecks(bot, canduelarray, commandortarget, instigator, currentduelplayersarray, inchannel)
    if not executedueling:
        bot.notice(executeduelingmsg,instigator)
        return
    if instigator in canduelarray:
        canduelarray.remove(instigator)
    dispmsgarray = []
    displaymessage = get_trigger_arg(canduelarray, "list")
    bot.say(instigator + " Initiated a full channel " + commandortarget + " event. Good luck to " + displaymessage)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget), now)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget + 'instigator'), instigator)
    totalplayers = len(canduelarray)
    riskcoins = int(totalplayers) * 30
    damage = riskcoins
    winner = selectwinner(bot, canduelarray)
    dispmsgarray.append("The Winner is: " + winner + "! Total winnings: " + str(riskcoins) + " coin! Losers took " + str(riskcoins) + " damage.")
    diedinbattle = []
    canduelarray.remove(winner)
    for x in canduelarray:
        damagescale = tierratio_level(bot)
        damage = damagescale * damage
        currentbodypartsarray = bodypartarray(bot, x)
        bodypart = get_trigger_arg(currentbodypartsarray, 'random')
        bodypartname = bodypart.split("_", 1)[1]
        damage, damagetextarray = damage_resistance(bot, x, damage, bodypart)
        for j in damagetextarray:
            dispmsgarray.append(j)
        if damage > 0:
            splitdamage = int(damage) / 6
            for part in stats_healthbodyparts:
                adjust_database_value(bot, x, part, -abs(splitdamage))
            xheadhealth = get_database_value(bot, x, 'health_head')
            xtorsohealth = get_database_value(bot, x, 'health_torso')
            if xheadhealth  <= 0 or xtorsohealth <= 0:
                winnertextarray = whokilledwhom(bot, winner, x)
                diedinbattle.append(x)
            else:
                for part in stats_healthbodyparts:
                    xcurrenthealthbody  = get_database_value(bot, x, part)
                    if xcurrenthealthbody  <= 0:
                        bodypartname = bodypart.split("_", 1)[1]
                        bodypartname = bodypartname.replace("_", " ")
                        dispmsgarray.append(loser + "'s " + bodypartname + " has become crippled!")
    if diedinbattle != []:
        displaymessage = get_trigger_arg(diedinbattle, "list")
        dispmsgarray.append(displaymessage + " died in this event.")
    adjust_database_value(bot, winner, 'loot_coin', riskcoins)
    onscreentext(bot, [inchannel], dispmsgarray)

## Assault
def subcommand_assault(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    if bot.nick in canduelarray:
        canduelarray.remove(bot.nick)
    executedueling, executeduelingmsg = eventchecks(bot, canduelarray, commandortarget, instigator, currentduelplayersarray, inchannel)
    if not executedueling:
        bot.notice(executeduelingmsg,instigator)
        return
    duelslockout = get_database_value(bot, duelrecorduser, 'duelslockout') or 0
    if duelslockout:
        lockoutsince = get_timesince_duels(bot, instigator, 'duelslockout')
        if lockoutsince < duel_lockout_timer:
            bot.notice(instigator + ", duel(s) is/are currently in progress. You must wait. If this is an error, it should clear itself in 5 minutes.", instigator)
            return
        reset_database_value(bot, duelrecorduser, 'duelslockout')
    set_database_value(bot, duelrecorduser, 'duelslockout', now)
    if instigator in canduelarray:
        canduelarray.remove(instigator)
    displaymessage = get_trigger_arg(canduelarray, "list")
    bot.say(instigator + " Initiated a full channel " + commandortarget + " event. Good luck to " + displaymessage)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget), now)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget + 'instigator'), instigator)
    lastfoughtstart = get_database_value(bot, instigator, 'record_lastfought')
    duel_combat(bot, instigator, instigator, canduelarray, triggerargsarray, now, inchannel, 'assault')
    set_database_value(bot, instigator, 'record_lastfought', lastfoughtstart)
    reset_database_value(bot, duelrecorduser, 'duelslockout')

    ## usage counter ## TODO use len(canduelarray)
    adjust_database_value(bot, instigator, 'usage_total', 1)
    adjust_database_value(bot, instigator, 'usage_combat', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_total', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_combat', 1)

## Random Target
def subcommand_random(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    if instigator not in canduelarray:
        canduel, validtargetmsg = duelcriteria(bot, instigator, commandortarget, currentduelplayersarray, inchannel)
        bot.notice(validtargetmsg,instigator)
        return
    if canduelarray == []:
        bot.notice(instigator + ", It looks like the full channel " + commandortarget + " event target finder has failed.", instigator)
        return
    duelslockout = get_database_value(bot, duelrecorduser, 'duelslockout') or 0
    if duelslockout:
        lockoutsince = get_timesince_duels(bot, instigator, 'duelslockout')
        if lockoutsince < duel_lockout_timer:
            bot.notice(instigator + ", duel(s) is/are currently in progress. You must wait. If this is an error, it should clear itself in 5 minutes.", instigator)
            return
        reset_database_value(bot, duelrecorduser, 'duelslockout')
    set_database_value(bot, duelrecorduser, 'duelslockout', now)
    if bot.nick not in canduelarray:
        canduelarray.append(bot.nick)
    target = get_trigger_arg(canduelarray, 'random')
    duel_combat(bot, instigator, instigator, [target], triggerargsarray, now, inchannel, 'random')
    reset_database_value(bot, duelrecorduser, 'duelslockout')

    ## usage counter
    adjust_database_value(bot, instigator, 'usage_total', 1)
    adjust_database_value(bot, instigator, 'usage_combat', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_total', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_combat', 1)

## Usage
def subcommand_usage(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    targetcom = get_trigger_arg(triggerargsarray, 2) or instigator
    targetcomname = targetcom
    if targetcom in commandarray_all_valid or targetcom == 'combat':
        target = get_trigger_arg(triggerargsarray, 3) or instigator
        targetname = target
        if target == 'channel':
            target = bot.nick
        totaluses = get_database_value(bot, target, 'usage_'+targetcom)
        target = actualname(bot, target)
        bot.say(targetname + " has used duel " + str(targetcom) + " " + str(totaluses) + " times.")
        return
    if targetcom == 'channel':
        targetcom = bot.nick
    validtarget, validtargetmsg = targetcheck(bot, targetcom, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
    if not validtarget and targetcom != bot.nick:
        bot.notice(validtargetmsg, instigator)
        return
    totaluses = get_database_value(bot, targetcom, 'usage_total')
    targetcom = actualname(bot, targetcomname)
    bot.say(targetcom + " has used duels " + str(totaluses) + " times.")

## War Room
def subcommand_warroom(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    subcommand = get_trigger_arg(triggerargsarray, 2).lower()
    if not subcommand:
        if instigator not in canduelarray:
            canduel, validtargetmsg = duelcriteria(bot, instigator, subcommand, currentduelplayersarray, inchannel)
            bot.notice(validtargetmsg,instigator)
        bot.notice(instigator + ", It looks like you can duel.", instigator)
    elif subcommand == 'colosseum' or subcommand == 'assault':
        ## TODO: alt commands
        executedueling, executeduelingmsg = eventchecks(bot, canduelarray, subcommand, instigator, currentduelplayersarray, inchannel)
        if not executedueling:
            bot.notice(executeduelingmsg,instigator)
        else:
            bot.notice(instigator + ", It looks like full channel " + subcommand + " event can be used.", instigator)
    elif subcommand == 'list':
        if instigator in canduelarray:
            canduelarray.remove(instigator)
        if bot.nick in canduelarray:
            canduelarray.remove(bot.nick)
        if canduelarray != []:
            displaymessage = get_trigger_arg(canduelarray, "list")
            bot.say(instigator + ", you may duel the following users: "+ str(displaymessage ))
        else:
            bot.notice(instigator + ", It looks like nobody can duel at the moment.",instigator)
    else:
        validtarget, validtargetmsg = targetcheck(bot, subcommand, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
        if not validtarget:
            bot.notice(validtargetmsg, instigator)
            return
        executedueling, executeduelingmsg = duelcriteria(bot, instigator, subcommand, currentduelplayersarray, inchannel)
        if not executedueling:
            bot.notice(executeduelingmsg,instigator)
            return
        subcommand = actualname(bot, subcommand)
        if subcommand in canduelarray and instigator in canduelarray:
            bot.notice(instigator + ", It looks like you can duel " + subcommand + ".", instigator)

## Title
def subcommand_title(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    instigatortitle = get_database_value(bot, instigator, 'title')
    titletoset = get_trigger_arg(triggerargsarray, "2+")
    if not titletoset:
        bot.notice(instigator + ", what do you want your title to be?", instigator)
    elif titletoset == 'remove':
        reset_database_value(bot, instigator, 'title')
        bot.notice(instigator + ", your title has been removed", instigator)
    else:
        titletoset = str(titletoset)
        instigatorcoin = get_database_value(bot, instigator, 'loot_coin') or 0
        if instigatorcoin < class_cost:
            bot.notice(instigator + ", changing your title costs " + str(title_cost) + " coin. You need more funding.", instigator)
        elif len(titletoset) > 10:
            bot.notice(instigator + ", purchased titles can be no longer than 10 characters", instigator)
        else:
            set_database_value(bot, instigator, 'title', titletoset)
            adjust_database_value(bot, instigator, 'loot_coin', -abs(title_cost))
            bot.say(instigator + ", your title is now " + titletoset)

## Class
def subcommand_class(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    subcommandarray = ['set','change']
    classes = get_trigger_arg(class_array, "list")
    subcommand = get_trigger_arg(triggerargsarray, 2).lower()
    setclass = get_trigger_arg(triggerargsarray, 3).lower()
    instigatorclass = get_database_value(bot, instigator, 'class_setting')
    instigatorfreebie = get_database_value(bot, instigator, 'class_freebie') or 0
    classtime = get_timesince_duels(bot, instigator, 'class_timeout')
    instigatorclasstime = get_timesince_duels(bot, instigator, 'class_timeout')
    instigatorcoin = get_database_value(bot, instigator, 'loot_coin') or 0
    if not instigatorclass and not subcommand:
        bot.say("You don't appear to have a class set. Options are : " + classes + ". Run .duel class set    to set your class.")
    elif not subcommand:
        bot.say("Your class is currently set to " + str(instigatorclass) + ". Use .duel class change    to change class. Options are : " + classes + ".")
    elif classtime < timeout_class and not inchannel in devenabledchannels:
        bot.say("You may not change your class more than once per 24 hours. Please wait "+str(hours_minutes_seconds((timeout_class - instigatorclasstime)))+" to change.")
    elif subcommand not in subcommandarray:
        bot.say("Invalid command. Options are set or change.")
    elif not setclass:
        bot.say("Which class would you like to use? Options are: " + classes +".")
    elif instigatorcoin < class_cost and instigatorfreebie:
        bot.say("Changing class costs " + str(class_cost) + " coin. You need more funding.")
    elif setclass not in class_array:
        bot.say("Invalid class. Options are: " + classes +".")
    elif setclass == instigatorclass:
        bot.say('Your class is already set to ' +  setclass)
    else:
        set_database_value(bot, instigator, 'class_setting', setclass)
        bot.say('Your class is now set to ' +  setclass)
        set_database_value(bot, instigator, 'class_timeout', now)
        if instigatorfreebie:
            adjust_database_value(bot, instigator, 'loot_coin', -abs(class_cost))
        else:
            set_database_value(bot, instigator, 'class_freebie', 1)

## Streaks
def subcommand_streaks(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    target = get_trigger_arg(triggerargsarray, 2) or instigator
    if int(tiercommandeval) > int(currenttier) and target != instigator:
        bot.notice(instigator + ", Stats for other players cannot be viewed until somebody reaches " + str(tierpepperrequired.title()) + ". "+str(tiermath) + " tier(s) remaining!", instigator)
        if not inchannel in devenabledchannels:
            return
    validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
    if not validtarget:
        bot.notice(validtargetmsg, instigator)
        return
    target = actualname(bot, target)
    streak_type = get_database_value(bot, target, 'streak_type_current') or 'none'
    best_wins = get_database_value(bot, target, 'streak_win_best') or 0
    worst_losses = get_database_value(bot, target, 'streak_loss_best') or 0
    if streak_type == 'win':
        streak_count = get_database_value(bot, target, 'streak_win_current') or 0
        typeofstreak = 'winning'
    elif streak_type == 'loss':
        streak_count = get_database_value(bot, target, 'streak_loss_current') or 0
        typeofstreak = 'losing'
    else:
        streak_count = 0
    dispmsgarray = []
    if streak_count > 1 and streak_type != 'none':
        dispmsgarray.append("Currently on a " + typeofstreak + " streak of " + str(streak_count) + ".")
    if int(best_wins) > 1:
        dispmsgarray.append("Best Win streak= " + str(best_wins) + ".")
    if int(worst_losses) > 1:
        dispmsgarray.append("Worst Losing streak= " + str(worst_losses) + ".")
    if dispmsgarray != []:
        dispmsgarrayb = []
        dispmsgarrayb.append(target + "'s streaks:")
        for x in dispmsgarray:
            dispmsgarrayb.append(x)
    else:
        dispmsgarrayb.append(target + " has no streaks.")
    onscreentext(bot, ['say'], dispmsgarrayb)

## Stats
def subcommand_stats(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    target = get_trigger_arg(triggerargsarray, 2) or instigator
    if int(tiercommandeval) > int(currenttier) and target != instigator:
        bot.notice(instigator + ", Stats for other players cannot be viewed until somebody reaches " + str(tierpepperrequired.title()) + ". "+str(tiermath) + " tier(s) remaining!", instigator)
        if not inchannel in devenabledchannels:
            return
    validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
    if not validtarget:
        bot.notice(validtargetmsg, instigator)
        return
    target = actualname(bot, target)
    dispmsgarray = []
    totalhealth = get_health(bot,target)
    if totalhealth:
        dispmsgarray.append("Health="+str(totalhealth))
    for x in stats_view:
        if x in stats_view_functions:
            scriptdef = str('get_' + x + '(bot,target)')
            gethowmany = eval(scriptdef)
        else:
            gethowmany = get_database_value(bot, target, x)
        if gethowmany:
            if x == 'winlossratio':
                gethowmany = format(gethowmany, '.3f')
            statname = x.title()
            dispmsgarray.append(statname + "=" + str(gethowmany))
                
    dispmsgarrayb = []
    if dispmsgarray != []:
        pepper = get_pepper(bot, target)
        if not pepper or pepper == '':
            targetname = target
        else:
            targetname = str("(" + str(pepper.title()) + ") " + target)
        dispmsgarrayb.append(targetname + "'s " + commandortarget + ":")
        for y in dispmsgarray:
            dispmsgarrayb.append(y)
    else:
        dispmsgarrayb.append(instigator + ", It looks like " + target + " has no " +  commandortarget + ".")
    onscreentext(bot, ['say'], dispmsgarrayb)

## Leaderboard
def subcommand_leaderboard(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    subcommand = get_trigger_arg(triggerargsarray, 2)
    if not subcommand:
        leaderscript = []
        leaderboardarraystats = ['winlossratio','record_kills','record_respawns','health','streak_win_best','streak_loss_best','bounty_amount']
        streak_loss_bestdispmsg, streak_loss_bestdispmsgb = "Worst Losing Streak:", ""
        winlossratiodispmsg, winlossratiodispmsgb = "Wins/Losses:", ""
        record_killsdispmsg, record_killsdispmsgb = "Most Kills:", "kills"
        record_respawnsdispmsg, record_respawnsdispmsgb = "Most Deaths:", "respawns"
        healthdispmsg, healthdispmsgb = "Closest To Death:", "health"
        streak_win_bestdispmsg, streak_win_bestdispmsgb = "Best Win Streak:", ""
        bounty_amountdispmsg, bounty_amountdispmsgb = "Largest Bounty:", "coins"
        for x in leaderboardarraystats:
            statleadername = ''
            if x != 'health':
                statleadernumber = 0
            else:
                statleadernumber = 99999999
            for u in currentduelplayersarray:
                if x != 'winlossratio' and x != 'health':
                    statamount = get_database_value(bot, u, x)
                else:
                    scriptdef = str('get_' + x + '(bot,u)')
                    statamount = eval(scriptdef)
                if statamount == statleadernumber and statamount > 0:
                    statleadername = str(statleadername+ " "+ u)
                else:
                    if x != 'health':
                        if statamount > statleadernumber:
                            statleadernumber = statamount
                            statleadername = u
                    else:
                        if statamount < statleadernumber and statamount > 0:
                            statleadernumber = statamount
                            statleadername = u
            if x == 'winlossratio':
                statleadernumber = format(statleadernumber, '.3f')
            if statleadername != '':
                msgtoadd = str(eval(x+"dispmsg") + " "+ statleadername + " at "+ str(statleadernumber)+ " "+ eval(x+"dispmsgb"))
                leaderscript.append(msgtoadd)
        if leaderscript == []:
            leaderscript.append("Leaderboard appears to be empty")
        onscreentext(bot, ['say'], leaderscript)
    if subcommand.lower() == 'highest' or subcommand.lower() == 'lowest':
        subcommand = subcommand.lower()
        subcommanda = get_trigger_arg(triggerargsarray, 3)
        if not subcommanda:
            bot.say("What stat do you want to check highest/losest?")
            return
        duelstatsadminarray = duels_valid_stats(bot)
        if subcommanda.lower() not in duelstatsadminarray and subcommanda.lower() != 'class':
            bot.say("This stat is either not comparable at the moment or invalid.")
        else:
            subcommanda = subcommanda.lower()
            statleadername = ''
            if subcommand == 'highest':
                statleadernumber = 0
            else:
                statleadernumber = 99999999
            for u in bot.users:
                if subcommanda != 'winlossratio':
                    statamount = get_database_value(bot, u, subcommanda)
                else:
                    scriptdef = str('get_' + subcommanda + '(bot,u)')
                    statamount = eval(scriptdef)
                if statamount == statleadernumber and statamount > 0:
                    statleadername = str(statleadername+ " "+ u)
                else:
                    if subcommand == 'highest':
                        if statamount > statleadernumber:
                            statleadernumber = statamount
                            statleadername = u
                    else:
                        if statamount < statleadernumber and statamount > 0:
                            statleadernumber = statamount
                            statleadername = u
            if statleadername != '':
                bot.say("The " + subcommand + " amount for "+ subcommanda+ " is " + statleadername+ " with "+ str(statleadernumber))
            else:
                bot.say("There doesn't appear to be a "+ subcommand + " amount for "+subcommanda+".")

## Armor ## TODO
def subcommand_armor(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    subcommand = get_trigger_arg(triggerargsarray, 2)
    typearmor = get_trigger_arg(triggerargsarray, 3)
    if not subcommand or subcommand.lower() in [x.lower() for x in dueloptedinarray]:
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
        if not validtarget:
            bot.notice(validtargetmsg, instigator)
            return
        target = actualname(bot, target)
        dispmsgarray = []
        for x in stats_armor:
            gethowmany = get_database_value(bot, target, x)
            if gethowmany:
                xname = x.split("_", 1)[1]
                xname = xname.replace("_", " ")
                xname = xname.title()
                dispmsgarray.append(str(xname) + "=" + str(gethowmany))
        dispmsgarrayb = []
        if dispmsgarray != []:
            dispmsgarrayb.append(target + "'s " + commandortarget + " durability:")
            for y in dispmsgarray:
                dispmsgarrayb.append(y)
        else:
            dispmsgarrayb.append(instigator + ", It looks like " + target + " has no " +  commandortarget + ".")
        onscreentext(bot, ['say'], dispmsgarrayb)
    elif subcommand == 'buy':
        instigatorcoin = get_database_value(bot, instigator, 'loot_coin') or 0
        if not typearmor or "armor_"+typearmor not in stats_armor:
            temparmorlistarray = []
            for x in stats_armor:
                armorname = x.split("_", 1)[1]
                temparmorlistarray.append(armorname)
            armors = get_trigger_arg(temparmorlistarray, 'list')
            bot.say("What type of armor do you wish to " + subcommand + "? Options are: " + armors)
        elif instigatorcoin < armor_cost:
            bot.say("Insufficient Funds")
        else:
            getarmor = get_database_value(bot, instigator, "armor_"+typearmor) or 0
            if getarmor and getarmor > 0:
                bot.say("It looks like you already have a " + typearmor + ".")
            else:
                bot.say(instigator + " bought " + typearmor + " for " + str(armor_cost) + " coins.")
                adjust_database_value(bot, instigator, 'loot_coin', -abs(armor_cost))
                set_database_value(bot, instigator, "armor_"+typearmor, armor_durability)
    elif subcommand == 'sell':
        if not typearmor or "armor_"+typearmor not in stats_armor:
            temparmorlistarray = []
            for x in stats_armor:
                armorname = x.split("_", 1)[1]
                temparmorlistarray.append(armorname)
            armors = get_trigger_arg(temparmorlistarray, 'list')
            bot.say("What type of armor do you wish to " + subcommand + "? Options are: " + armors)
        else:
            getarmor = get_database_value(bot, instigator, "armor_"+typearmor) or 0
            if not getarmor:
                bot.say("You don't have a " + typearmor + " to sell.")
            elif getarmor < 0:
                bot.say("Your armor is too damaged to sell.")
                reset_database_value(bot, instigator, "armor_"+typearmor)
            else:
                durabilityremaining = getarmor / armor_durability
                sellingamount = durabilityremaining * armor_cost
                if sellingamount <= 0:
                    bot.say("Your armor is too damaged to sell.")
                else:
                    bot.say("Selling your "+typearmor +" earned you " + str(sellingamount) + " coins.")
                    adjust_database_value(bot, instigator, 'loot_coin', sellingamount)
                    reset_database_value(bot, instigator, "armor_"+typearmor)
    elif subcommand == 'repair':
        if not typearmor or "armor_"+typearmor not in stats_armor:
            temparmorlistarray = []
            for x in stats_armor:
                armorname = x.split("_", 1)[1]
                temparmorlistarray.append(armorname)
            armors = get_trigger_arg(temparmorlistarray, 'list')
            bot.say("What type of armor do you wish to " + subcommand + "? Options are: " + armors)
        else:
            getarmor = get_database_value(bot, instigator, "armor_"+typearmor) or 0
            instigatorclass = get_database_value(bot, instigator, 'class_setting')
            durabilitycompare = armor_durability
            if instigatorclass == 'blacksmith':
                durabilitycompare = armor_durability_blacksmith
            if not getarmor:
                bot.say("You don't have a " + typearmor + " to repair.")
            elif getarmor >= durabilitycompare:
                bot.say("It looks like your armor does not need repair.")
            else:
                durabilitytorepair = durabilitycompare - getarmor
                if durabilitytorepair <= 0:
                    bot.say("Looks like you can't repair that right now.")
                else:
                    instigatorcoin = get_database_value(bot, instigator, 'loot_coin') or 0
                    costinvolved  = durabilitytorepair / durabilitycompare
                    costinvolved = costinvolved * armor_cost
                    if instigatorcoin < costinvolved:
                        bot.say("Insufficient Funds.")
                    else:
                        bot.say(typearmor + " repaired  for " + str(costinvolved)+" coins.")
                        adjust_database_value(bot, instigator, 'loot_coin', -abs(costinvolved))
                        set_database_value(bot, instigator, "armor_"+typearmor, durabilitycompare)

## Bounty ## TODO
def subcommand_bounty(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    if not inchannel.startswith("#"):
        bot.notice(instigator + " Bounties must be in channel.", instigator)
        return
    instigatorcoin = get_database_value(bot, instigator, 'loot_coin') or 0
    target = get_trigger_arg(triggerargsarray, 2)
    validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
    if not validtarget:
        bot.notice(validtargetmsg, instigator)
        return
    target = actualname(bot, target)
    amount = get_trigger_arg(triggerargsarray, 3)
    if not amount.isdigit():
        bot.say("Invalid Amount.")
        return
    amount = int(amount)
    if not amount:
        bot.say("How much of a bounty do you wish to place on "+target+".")
    elif int(instigatorcoin) < int(amount):
        bot.say("Insufficient Funds.")
    else:
        adjust_database_value(bot, instigator, 'loot_coin', -abs(amount))
        bountyontarget = get_database_value(bot, target, 'bounty_amount') or 0
        if not bountyontarget:
           bot.say(instigator + " places a bounty of " + str(amount) + " on " + target)
        else:
           bot.say(instigator + " adds " + str(amount) + " to the bounty on " + target)
        adjust_database_value(bot, target, 'bounty_amount', amount)

## Loot ## TODO
def subcommand_loot(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    instigatorclass = get_database_value(bot, instigator, 'class_setting')
    instigatorcoin = get_database_value(bot, instigator, 'loot_coin') or 0
    lootcommand = get_trigger_arg(triggerargsarray, 2).lower()
    if not lootcommand or lootcommand.lower() in [x.lower() for x in dueloptedinarray]:
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        if int(tiercommandeval) > int(currenttier) and target != instigator:
            bot.notice(instigator + ", Stats for other players cannot be viewed until somebody reaches " + str(tierpepperrequired.title()) + ". "+str(tiermath) + " tier(s) remaining!", instigator)
            if not inchannel in devenabledchannels:
                return
        validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
        if not validtarget:
            bot.notice(validtargetmsg, instigator)
            return
        target = actualname(bot, target)
        dispmsgarray = []
        for x in loot_view:
            gethowmany = get_database_value(bot, target, x)
            if gethowmany:
                xname = x.split("_", 1)[1]
                xname = xname.replace("_", " ")
                xname = xname.title()
                if gethowmany == 1:
                    loottype = str(xname)
                else:
                    loottype = str(str(xname)+"s")
                dispmsgarray.append(str(loottype) + "=" + str(gethowmany))
        dispmsgarrayb = []
        if dispmsgarray != []:
            dispmsgarrayb.append(target + "'s " + commandortarget + ":")
            for y in dispmsgarray:
                dispmsgarrayb.append(y)
        else:
            dispmsgarrayb.append(instigator + ", It looks like " + target + " has no " +  commandortarget + ".")
        onscreentext(bot, ['say'], dispmsgarrayb)
    elif lootcommand == 'use':
        lootitem = get_trigger_arg(triggerargsarray, 3).lower()
        gethowmanylootitem = get_database_value(bot, instigator, "loot_"+lootitem) or 0
        if not lootitem:
            bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
        elif lootitem not in potion_types and lootitem != 'grenade':
            bot.notice(instigator + ", Invalid loot item.", instigator)
        elif not gethowmanylootitem:
            bot.notice(instigator + ", You do not have any " +  lootitem + "!", instigator)
        elif lootitem == 'magicpotion':
            bot.notice("Magic Potions are not purchasable, sellable, or usable. They can only be traded.", instigator)
        elif lootitem == 'grenade':
            if not inchannel.startswith("#"):
                bot.notice(instigator + ", grenades must be used in channel.", instigator)
                return
            instigatorgrenade = get_database_value(bot, instigator, 'loot_grenade') or 0
            if instigator in canduelarray:
                canduelarray.remove(instigator)
            if bot.nick in canduelarray:
                canduelarray.remove(bot.nick)
            if canduelarray == []:
                bot.notice(instigator + ", It looks like using a grenade right now won't hurt anybody.", instigator)
            else:
                dispmsgarray = []
                adjust_database_value(bot, instigator, "loot_"+lootitem, -1)
                fulltarget, secondarytarget, thirdtarget = '','',''
                fulltarget = get_trigger_arg(canduelarray, "random")
                dispmsgarray.append(fulltarget + " takes the brunt of the grenade dealing " + str(abs(grenade_full_damage)) + " damage.")
                canduelarray.remove(fulltarget)
                if canduelarray != []:
                    secondarytarget = get_trigger_arg(canduelarray, "random")
                    canduelarray.remove(secondarytarget)
                    if canduelarray != []:
                        thirdtarget = get_trigger_arg(canduelarray, "random")
                        dispmsgarray.append(secondarytarget + " and " + thirdtarget + " jump away but still take " + str(abs(grenade_secondary_damage)) + " damage.")
                        canduelarray.remove(thirdtarget)
                        if canduelarray != []:
                            remainingarray = get_trigger_arg(canduelarray, "list")
                            dispmsgarray.append(remainingarray + " completely jump out of the way")
                    else:
                        dispmsgarray.append(secondarytarget + " jumps away but still takes " + str(abs(grenade_secondary_damage)) + " damage.")
                painarray = []
                damagearray = []
                deatharray = []
                if fulltarget != '':
                    painarray.append(fulltarget)
                    damagearray.append(grenade_full_damage)
                if secondarytarget != '':
                    painarray.append(secondarytarget)
                    damagearray.append(grenade_secondary_damage)
                if thirdtarget != '':
                    painarray.append(thirdtarget)
                    damagearray.append(grenade_secondary_damage)
                diedinbattle = []
                for player, damage in zip(painarray, damagearray):
                    damage = int(damage)
                    damagescale = tierratio_level(bot)
                    damage = damagescale * damage
                    bodypart = get_trigger_arg(stats_healthbodyparts, 'random')
                    bodypartname = bodypart.split("_", 1)[1]
                    damage, damagetextarray = damage_resistance(bot, player, damage, bodypart, bodypartname)
                    for j in damagetextarray:
                        dispmsgarray.append(j)
                    if damage > 0:
                        splitdamage = int(damage) / 6
                        for part in stats_healthbodyparts:
                            adjust_database_value(bot, x, part, -abs(splitdamage))
                        loserheadhealth = get_database_value(bot, loser, 'health_head')
                        losertorsohealth = get_database_value(bot, loser, 'health_torso')
                        if loserheadhealth  <= 0 or losertorsohealth <= 0:
                            winnertextarray = whokilledwhom(bot, instigator, player)
                            diedinbattle.append(player)
                        else:
                            for part in stats_healthbodyparts:
                                losercurrenthealthbody  = get_database_value(bot, loser, part)
                                if losercurrenthealthbody  <= 0:
                                    bodypartname = bodypart.split("_", 1)[1]
                                    bodypartname = bodypartname.replace("_", " ")
                                    dispmsgarray.append(loser + "'s " + bodypartname + " has become crippled!")
                if diedinbattle != []:
                    displaymessage = get_trigger_arg(diedinbattle, "list")
                    dispmsgarray.append(displaymessage + " died by this grenade volley.")
                onscreentext(bot, [inchannel], dispmsgarray)
        else:
            targnum = get_trigger_arg(triggerargsarray, 4).lower()
            if not targnum:
                quantity = 1
                target = instigator
            elif targnum.isdigit():
                quantity = int(targnum)
                target = instigator
            elif targnum.lower() in [x.lower() for x in dueloptedinarray]:
                targnumb = get_trigger_arg(triggerargsarray, 5).lower()
                target = targnum
                if not targnumb:
                    quantity = 1
                elif targnumb.isdigit():
                    quantity = int(targnumb)
                elif targnumb == 'all':
                    quantity = int(gethowmanylootitem)
                else:
                    bot.say("Invalid command.")
                    return
            elif targnum == 'all':
                target = instigator
                quantity = int(gethowmanylootitem)
            else:
                bot.say("Invalid command.")
                return
            if not quantity:
                bot.say("Invalid command.")
                return
            if target == bot.nick:
                bot.notice(instigator + ", I am immune to " + lootitem, instigator)
                return
            validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
            if not validtarget:
                bot.notice(validtargetmsg, instigator)
                return
            target = actualname(bot, target)
            targetclass = get_database_value(bot, target, 'class_setting') or 'notclassy'
            if int(gethowmanylootitem) < int(quantity):
                bot.notice(instigator + ", You do not have enough " +  lootitem + " to use this command!", instigator)
                return
            if target.lower() != instigator.lower() and targetclass == 'fiend':
                bot.notice(instigator + ", It looks like " + target + " is a fiend and can only self-use potions.", instigator)
                adjust_database_value(bot, instigator, "loot_"+lootitem, -abs(quantity))
                return
            uselootarray = []
            adjust_database_value(bot, instigator, "loot_"+lootitem, -abs(quantity))
            lootusedeaths = 0
            if lootitem == 'mysterypotion':
                while int(quantity) > 0:
                    quantity = quantity - 1
                    loot = get_trigger_arg(potion_types, 'random')
                    if loot == 'mysterypotion' or loot == 'magicpotion':
                        loot = get_trigger_arg(loot_null, 'random')
                    uselootarray.append(loot)
            else:
                while int(quantity) > 0:
                    quantity = quantity - 1
                    uselootarray.append(lootitem)
            uselootarraytotal = len(uselootarray)
            extramsg = '.'
            if lootitem == 'healthpotion':
                if targetclass == 'barbarian':
                    potionmaths = int(uselootarraytotal) * healthpotion_worth_barbarian
                else:
                    potionmaths = int(uselootarraytotal) * healthpotion_worth
                extramsg = str(" restoring " + str(potionmaths) + " health.")
            elif lootitem == 'poisonpotion':
                poisonpotionworthb = abs(poisonpotion_worth)
                potionmaths = int(uselootarraytotal) * int(poisonpotionworthb)
                extramsg = str(" draining " + str(potionmaths) + " health.")
            elif lootitem == 'manapotion':
                if targetclass == 'mage':
                    potionmaths = int(uselootarraytotal) * manapotion_worth_mage
                else:
                    potionmaths = int(uselootarraytotal) * manapotion_worth
                extramsg = str(" restoring " + str(potionmaths) + " mana.")
            elif lootitem == 'timepotion':
                extramsg = str(" removing timeouts.")
            if target == instigator:
                if int(uselootarraytotal) == 1:
                    mainlootusemessage = str(instigator + ' uses ' + lootitem + extramsg)
                else:
                    mainlootusemessage = str(instigator + ' uses ' + str(uselootarraytotal) + " " + lootitem + 's' + extramsg)
            else:
                if int(uselootarraytotal) == 1:
                    mainlootusemessage = str(instigator + ' uses ' + lootitem + ' on ' + target + extramsg)
                else:
                    mainlootusemessage = str(instigator + " used " + str(uselootarraytotal) + " " + lootitem + "s on " + target +extramsg)
            for x in uselootarray:
                if x == 'healthpotion':
                    if targetclass == 'barbarian':
                        splitdamage = healthpotion_worth_barbarian / 6
                        for part in stats_healthbodyparts:
                            adjust_database_value(bot, target, part, splitdamage)
                    else:
                        splitdamage = healthpotion_worth / 6
                        for part in stats_healthbodyparts:
                            adjust_database_value(bot, target, part, splitdamage)
                elif x == 'poisonpotion':
                    splitdamage = poisonpotion_worth / 6
                    for part in stats_healthbodyparts:
                        adjust_database_value(bot, target, part, splitdamage)
                elif x == 'manapotion':
                    if targetclass == 'mage':
                        adjust_database_value(bot, target, 'magic_mana', manapotion_worth_mage)
                    else:
                        adjust_database_value(bot, target, 'magic_mana', manapotion_worth)
                elif x == 'timepotion':
                    reset_database_value(bot, target, 'record_lastfought')
                    for k in timepotiontargetarray:
                        targetequalcheck = get_database_value(bot, bot.nick, k) or bot.nick
                        if targetequalcheck == target:
                            reset_database_value(bot, bot.nick, k)
                    for j in timepotiontimeoutarray:
                        reset_database_value(bot, target, j)
                    reset_database_value(bot, bot.nick, 'timeout_timeout')
                    targetheadhealth = get_database_value(bot, target, 'health_head')
                    targettorsohealth = get_database_value(bot, target, 'health_torso')
                    if targetheadhealth  <= 0 or targettorsohealth <= 0:
                        if target == instigator:
                            deathmsgb = suicidekill(bot,loser) ## TODO array
                        else:
                            deathmsgb = whokilledwhom(bot, instigator, target) or ''  ## TODO array
                        lootusedeaths = lootusedeaths + 1
                        mainlootusemessage = str(mainlootusemessage + " "+ deathmsgb)
            if lootitem == 'mysterypotion':
                actualpotionmathedarray = []
                alreadyprocessedarray = []
                for fluid in uselootarray:
                    if fluid not in alreadyprocessedarray:
                        alreadyprocessedarray.append(fluid)
                        countedeval = uselootarray.count(fluid)
                        if countedeval > 1:
                           actualpotionmathedarray.append(str(str(countedeval) + " "+fluid + "s"))
                        else:
                            actualpotionmathedarray.append(fluid)
                postionsusedarray = get_trigger_arg(actualpotionmathedarray, "list")
                mainlootusemessage = str(mainlootusemessage + " Potion(s) used: " + postionsusedarray)
            if lootusedeaths > 0:
                if lootusedeaths == 1:
                    mainlootusemessage = str(mainlootusemessage + " This resulted in death.")
                else:
                    mainlootusemessage = str(mainlootusemessage + " This resulted in "+str(lootusedeaths)+" deaths.")
            bot.say(mainlootusemessage)
            if target != instigator and not inchannel.startswith("#"):
                bot.notice(mainlootusemessage, target)
    elif lootcommand == 'buy':
        lootitem = get_trigger_arg(triggerargsarray, 3).lower()
        if not lootitem:
            bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
        elif lootitem not in potion_types and lootitem != 'grenade':
            bot.notice(instigator + ", Invalid loot item.", instigator)
        elif lootitem == 'magicpotion':
            bot.say("Magic Potions are not purchasable, sellable, or usable. They can only be traded.")
        else:
            quantity = get_trigger_arg(triggerargsarray, 4).lower() or 1
            if quantity == 'all':
                if instigatorclass == 'scavenger':
                    quantity = int(instigatorcoin) / loot_buy_scavenger
                else:
                    quantity = int(instigatorcoin) / loot_buy_scavenger
                if not quantity > 1:
                    bot.notice(instigator + ", You do not have enough coin for this action.", instigator)
                    return
            quantity = int(quantity)
            if instigatorclass == 'scavenger':
                coinrequired = loot_buy_scavenger * int(quantity)
            else:
                coinrequired = loot_buy * int(quantity)
            if instigatorcoin < coinrequired:
                bot.notice(instigator + ", You do not have enough coin for this action.", instigator)
            else:
                adjust_database_value(bot, instigator, 'loot_coin', -abs(coinrequired))
                adjust_database_value(bot, instigator, "loot_"+lootitem, quantity)
                bot.say(instigator + " bought " + str(quantity) +  " "+lootitem + "s for " +str(coinrequired)+ " coins.")
    elif lootcommand == 'sell':
        lootitem = get_trigger_arg(triggerargsarray, 3).lower()
        gethowmanylootitem = get_database_value(bot, instigator, "loot_"+lootitem) or 0
        if not lootitem:
            bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
        elif lootitem not in potion_types and lootitem != 'grenade':
            bot.notice(instigator + ", Invalid loot item.", instigator)
        elif not gethowmanylootitem:
            bot.notice(instigator + ", You do not have any " +  lootitem + "!", instigator)
        elif lootitem == 'magicpotion':
            bot.say("Magic Potions are not purchasable, sellable, or usable. They can only be traded.")
        else:
            quantity = get_trigger_arg(triggerargsarray, 4).lower() or 1
            if quantity == 'all':
                quantity = gethowmanylootitem
            if int(quantity) > gethowmanylootitem:
                bot.notice(instigator + ", You do not have enough " + lootitem + " for this action.", instigator)
            else:
                quantity = int(quantity)
                if instigatorclass == 'scavenger':
                    reward = loot_sell_scavenger * int(quantity)
                else:
                    reward = loot_sell * int(quantity)
                adjust_database_value(bot, instigator, 'loot_coin', reward)
                adjust_database_value(bot, instigator, "loot_"+lootitem, -abs(quantity))
                bot.say(instigator + " sold " + str(quantity) + " "+ lootitem + "s for " +str(reward)+ " coins.")
    elif lootcommand == 'trade':
        lootitem = get_trigger_arg(triggerargsarray, 3).lower()
        lootitemb = get_trigger_arg(triggerargsarray, 4).lower()
        if not lootitem or not lootitemb:
            bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
        elif lootitem not in potion_types or lootitemb not in potion_types:
            bot.notice(instigator + ", Invalid loot item.", instigator)
        elif lootitem == 'grenade' or lootitemb == 'grenade':
            bot.notice(instigator + ", You can't trade for grenades.", instigator)
        elif lootitemb == lootitem:
            bot.notice(instigator + ", You can't trade for the same type of potion.", instigator)
        else:
            gethowmanylootitem = get_database_value(bot, instigator, lootitem) or 0
            quantity = get_trigger_arg(triggerargsarray, 5).lower() or 1
            if lootitem == 'magicpotion':
                tradingratio = 1
            elif instigatorclass == 'scavenger':
                tradingratio = loot_trade_scavenger
            else:
                tradingratio = loot_trade
            if quantity == 'all':
                quantity = gethowmanylootitem / tradingratio
            if quantity < 0:
                bot.notice(instigator + ", You do not have enough "+lootitem+" for this action.", instigator)
                return
            quantitymath = tradingratio * int(quantity)
            if gethowmanylootitem < quantitymath:
                bot.notice(instigator + ", You don't have enough of this item to trade.", instigator)
            else:
                adjust_database_value(bot, instigator, "loot_"+lootitem, -abs(quantitymath))
                adjust_database_value(bot, instigator, "loot_"+lootitemb, quantity)
                quantity = int(quantity)
                bot.say(instigator + " traded " + str(quantitymath) + " "+ lootitem + "s for " +str(quantity) + " "+ lootitemb+ "s.")
    else:
        transactiontypesarraylist = get_trigger_arg(loot_transaction_types, "list")
        bot.notice(instigator + ", It looks like " + lootcommand + " is either not here, not a valid person, or an invalid command. Valid commands are: " + loot_transaction_typeslist, instigator)

## Weaponslocker ## TODO
def subcommand_weaponslocker(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    target = get_trigger_arg(triggerargsarray, 2) or instigator
    validdirectionarray = ['total','inv','add','del','reset']
    if target in validdirectionarray:
        target = instigator
        adjustmentdirection = get_trigger_arg(triggerargsarray, 2).lower()
        weaponchange = get_trigger_arg(triggerargsarray, '3+')
    else:
        adjustmentdirection = get_trigger_arg(triggerargsarray, 3).lower()
        weaponchange = get_trigger_arg(triggerargsarray, '4+')
    weaponslist = get_database_value(bot, target, 'weaponslocker_complete') or []
    validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
    if not validtarget:
        bot.notice(validtargetmsg, instigator)
        return
    target = actualname(bot, target)
    if not adjustmentdirection:
        bot.notice(instigator + ", Use .duel weaponslocker add/del to adjust Locker Inventory.", instigator)
    elif adjustmentdirection == 'total':
        gethowmany = get_database_array_total(bot, target, 'weaponslocker_complete')
        bot.say(target + ' has ' + str(gethowmany) + " weapons in their locker. They Can be viewed in privmsg by running .duel weaponslocker inv")
    elif adjustmentdirection == 'inv':
        if weaponslist == []:
            bot.notice(instigator + ", There doesnt appear to be anything in the weapons locker! Use .duel weaponslocker add/del to adjust Locker Inventory.", instigator)
            return
        howmanyweapons = len(weaponslist)
        weaponsonscreenarray = []
        for weapon in weaponslist:
            howmanyweapons = howmanyweapons - 1
            if howmanyweapons > 0:
                weapon = str(weapon+",")
            weaponsonscreenarray.append(weapon)
        onscreentext(bot, [instigator], weaponsonscreenarray)
    elif target != instigator and not trigger.admin:
        bot.notice(instigator + ", You may not adjust somebody elses locker.", instigator)
    elif adjustmentdirection == 'reset':
        reset_database_value(bot, target, 'weaponslocker_complete')
        bot.notice(instigator + ", Locker Reset.", instigator)
    else:
        if not weaponchange:
            bot.notice(instigator + ", What weapon would you like to add/remove?", instigator)
        elif adjustmentdirection != 'add' and adjustmentdirection != 'del':
            bot.say('Invalid Command.')
        elif adjustmentdirection == 'add' and weaponchange in weaponslist:
            bot.notice(weaponchange + " is already in weapons locker.", instigator)
        elif adjustmentdirection == 'del' and weaponchange not in weaponslist:
            bot.notice(weaponchange + " is already not in weapons locker.", instigator)
        elif adjustmentdirection == 'add' and len(weaponchange) > weapon_name_length:
            bot.notice("That weapon exceeds the character limit of "+str(weapon_name_length)+".", instigator)
        else:
            if adjustmentdirection == 'add':
                weaponlockerstatus = 'now'
            else:
                weaponlockerstatus = 'no longer'
            adjust_database_array(bot, target, [weaponchange], 'weaponslocker_complete', adjustmentdirection)
            message = str(weaponchange + " is " + weaponlockerstatus + " in weapons locker.")
            bot.notice(instigator + ", " + message, instigator)

## Magic ## TODO
def subcommand_magic(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    instigatorclass = get_database_value(bot, instigator, 'class_setting')
    instigatormana = get_database_value(bot, instigator, 'magic_mana')
    magicusage = get_trigger_arg(triggerargsarray, 2)
    if not magicusage or magicusage not in magic_types:
        magicoptions = get_trigger_arg(magic_types, 'list')
        bot.say('Magic uses include: '+ magicoptions)
    else:
        targnum = get_trigger_arg(triggerargsarray, 3).lower()
        if not targnum:
            quantity = 1
            target = instigator
        elif targnum.isdigit():
            quantity = int(targnum)
            target = instigator
        elif targnum.lower() in [x.lower() for x in dueloptedinarray]:
            targnumb = get_trigger_arg(triggerargsarray, 4).lower()
            target = targnum
            if not targnumb:
                quantity = 1
            elif targnumb.isdigit():
                quantity = int(targnumb)
            elif targnumb == 'all':
                quantity = int(gethowmanylootitem)
            else:
                bot.say("Invalid command.")
                return
        if not instigatormana:
            bot.notice(instigator + " you don't have any mana.", instigator)
            return
        validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray)
        if not validtarget:
            bot.notice(validtargetmsg, instigator)
            return
        if target == bot.nick:
            bot.notice(instigator + ", I am immune to magic " + magicusage, instigator)
            return
        target = actualname(bot, target)
        targetclass = get_database_value(bot, target, 'class_setting') or 'notclassy'
        if target.lower() != instigator.lower() and targetclass == 'fiend':
            bot.notice(instigator + ", It looks like " + target + " is a fiend and can only self-use magic.", instigator)
            manarequired = -abs(manarequired)
            adjust_database_value(bot, instigator, 'magic_mana', manarequired)
            return
        targetcurse = get_database_value(bot, target, 'magic_curse') or 0
        if magicusage == 'curse' and targetcurse:
            bot.notice(instigator + " it looks like " + target + " is already cursed.", instigator)
            return
        if magicusage == 'curse':
            manarequired = magic_mana_required_curse
        elif magicusage == 'shield':
            manarequired = magic_mana_required_shield
        else:
            return
        if instigatorclass == 'mage':
            manarequired = manarequired * magic_usage_mage
        actualmanarequired = int(manarequired) * int(quantity)
        if int(actualmanarequired) > int(instigatormana):
            manamath = int(int(actualmanarequired) - int(instigatormana))
            bot.notice(instigator + " you need " + str(manamath) + " more mana to use magic " + magicusage + ".", instigator)
        else:
            specialtext = ''
            manarequired = -abs(actualmanarequired)
            adjust_database_value(bot, instigator, 'magic_mana', manarequired)
            if magicusage == 'curse':
                damagedealt = magic_curse_damage * int(quantity)
                set_database_value(bot, target, 'magic_curse', magic_curse_duration)
                specialtext = str("which forces " + target + " to lose the next " + str(magic_curse_duration) + " duels.")
                splitdamage = int(damagedealt) / 6
                for part in stats_healthbodyparts:
                    adjust_database_value(bot, target, part, -abs(splitdamage))
            elif magicusage == 'shield':
                damagedealt = magic_shield_health * int(quantity)
                actualshieldduration = int(quantity) * int(magic_shield_duration)
                adjust_database_value(bot, target, 'magic_shield', actualshieldduration)
                specialtext = str("which allows " + target + " to take no damage for the duration of " + str(actualshieldduration) + " damage AND restoring " +str(abs(damagedealt)) + " health.")
                splitdamage = int(damagedealt) / 6
                for part in stats_healthbodyparts:
                    adjust_database_value(bot, target, part, splitdamage)
            if instigator == target:
                displaymsg = str(instigator + " uses magic " + magicusage + " " + specialtext + ".")
            else:
                displaymsg = str(instigator + " uses magic " + magicusage + " on " + target + " " + specialtext + ".")
            bot.say(str(displaymsg))
            if not inchannel.startswith("#") and target != instigator:
                bot.notice(str(displaymsg), target)
            instigatormana = get_database_value(bot, instigator, 'magic_mana')
            if instigatormana <= 0:
                reset_database_value(bot, instigator, 'magic_mana')

## Admin ## TODO
def subcommand_admin(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels):
    subcommand = get_trigger_arg(triggerargsarray, 2).lower()
    if subcommand not in commandarray_all_valid and subcommand != 'bugbounty' and subcommand != 'channel':
        bot.notice(instigator + ", What Admin adjustment do you want to make?", instigator)
        return
    if subcommand == 'on' or subcommand == 'off':
        target = get_trigger_arg(triggerargsarray, 3).lower() or instigator
        if target == 'everyone':
            if subcommand == 'on':
                adjust_database_array(bot, duelrecorduser, botvisibleusers, 'duelusers', 'add')
            else:
                reset_database_value(bot, duelrecorduser, 'duelusers')
            bot.notice(instigator + ", duels should now be " +  subcommand + ' for ' + target + '.', instigator)
            return
        if target not in [y.lower() for y in botvisibleusers]:
            bot.notice(instigator + ", I have never seen " + str(target) + " before.", instigator)
            return
        target = actualname(bot, target)
        if subcommand == 'on' and target.lower() in [x.lower() for x in dueloptedinarray]:
            bot.notice(instigator + ", It looks like " + target + " already has duels on.", instigator)
            return
        if subcommand == 'off' and target.lower() not in [x.lower() for x in dueloptedinarray]:
            bot.notice(instigator + ", It looks like " + target + " already has duels off.", instigator)
            return
        if subcommand == 'on':
            adjust_database_array(bot, duelrecorduser, [target], 'duelusers', 'add')
        else:
            adjust_database_array(bot, duelrecorduser, [target], 'duelusers', 'del')
        set_database_value(bot, target, 'timeout_opttime', now)
        bot.notice(instigator + ", duels should now be " +  subcommand + ' for ' + target + '.', instigator)
    elif subcommand == 'tier':
        command = get_trigger_arg(triggerargsarray, 3).lower()
        if not command:
            bot.notice(instigator + ", what did you intend to do with tiers?")
            return
        target = get_trigger_arg(triggerargsarray, 4).lower() or instigator
        if target == 'channel':
            target = duelrecorduser
        if command == 'view':
            viewedtier = get_database_value(bot, target, 'leveling_tier')
            bot.notice(instigator + ", " + str(target) + " is at tier " + str(viewedtier) + ".", instigator)
        elif command == 'reset':
            bot.notice(instigator + ", " +  str(target) + "'s tier has been reset.", instigator)
            reset_database_value(bot, target, 'leveling_tier')
        elif command == 'set':
            newsetting = get_trigger_arg(triggerargsarray, 5)
            if not newsetting or not newsetting.isdigit():
                bot.notice(instigator + ", you must specify a number setting.", instigator)
                return
            bot.notice(instigator + ", " +  str(target) + "'s tier has been set to " + str(newsetting) + ".", instigator)
            set_database_value(bot, target, 'leveling_tier', int(newsetting))
        else:
            bot.notice(instigator + ", This looks to be an invalid command.")
    elif subcommand == 'bugbounty':
        target = get_trigger_arg(triggerargsarray, 3).lower() or instigator
        bot.say(target + ' is awarded ' + str(bugbounty_reward) + " coin for finding a bug in duels.")
        adjust_database_value(bot, target, 'loot_coin', bugbounty_reward)
    elif subcommand == 'roulette':
        command = get_trigger_arg(triggerargsarray, 3).lower()
        if command != 'reset':
            bot.notice(instigator + ", what did you intend to do with roulette?", instigator)
            return
        bot.notice(instigator + ", Roulette should now be reset.", instigator)
        reset_database_value(bot, duelrecorduser, 'roulettelastplayer')
        reset_database_value(bot, duelrecorduser, 'roulettechamber')
        reset_database_value(bot, duelrecorduser, 'roulettewinners')
        reset_database_value(bot, duelrecorduser, 'roulettecount')
        reset_database_value(bot, duelrecorduser, 'roulettespinarray')
        for user in botvisibleusers:
            reset_database_value(bot, user, 'roulettepayout')
    elif subcommand == 'stats':
        incorrectdisplay = "A correct command use is .duel admin stats target set/reset stat"
        target = get_trigger_arg(triggerargsarray, 3)
        subcommand = get_trigger_arg(triggerargsarray, 4)
        statset = get_trigger_arg(triggerargsarray, 5)
        newvalue = get_trigger_arg(triggerargsarray, 6)
        duelstatsadminarray = duels_valid_stats(bot)
        if not target:
            bot.notice(instigator + ", Target Missing. " + incorrectdisplay, instigator)
        elif target.lower() not in [u.lower() for u in botvisibleusers] and target != 'everyone':
            bot.notice(instigator + ", It looks like " + str(target) + " is either not here, or not a valid person.", instigator)
        elif not subcommand:
            bot.notice(instigator + ", Subcommand Missing. " + incorrectdisplay, instigator)
        elif subcommand not in stat_admin_commands:
            bot.notice(instigator + ", Invalid subcommand. " + incorrectdisplay, instigator)
        elif not statset:
            bot.notice(instigator + ", Stat Missing. " + incorrectdisplay, instigator)
        elif statset not in duelstatsadminarray and statset != 'all':
            bot.notice(instigator + ", Invalid stat. " + incorrectdisplay, instigator)
        else:
            target = actualname(bot, target)
            if subcommand == 'reset':
                newvalue = None
            if subcommand == 'set' and newvalue == None:
                bot.notice(instigator + ", When using set, you must specify a value. " + incorrectdisplay, instigator)
            elif target == 'everyone':
                set_database_value(bot, duelrecorduser, 'chanstatsreset', now)
                reset_database_value(bot, duelrecorduser, 'leveling_tier')
                reset_database_value(bot, duelrecorduser, 'specevent')
                for u in botvisibleusers:
                    if statset == 'all':
                         for x in duelstatsadminarray:
                             set_database_value(bot, u, x, newvalue)
                    else:
                        set_database_value(bot, u, statset, newvalue)
                bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)
            else:
                try:
                    if newvalue.isdigit():
                        newvalue = int(newvalue)
                except AttributeError:
                    newvalue = newvalue
                if statset == 'all':
                    for x in duelstatsadminarray:
                        set_database_value(bot, target, x, newvalue)
                else:
                    set_database_value(bot, target, statset, newvalue)
                bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)
    elif subcommand == 'channel':
        settingchange = get_trigger_arg(triggerargsarray, 3)
        if not settingchange:
            bot.notice(instigator + ", What channel setting do you want to change?", instigator)
        elif settingchange == 'statreset':
            set_database_value(bot, duelrecorduser, 'chanstatsreset', now)
        elif settingchange == 'lastassault':
            reset_database_value(bot, duelrecorduser, 'lastfullroomassultinstigator')
            bot.notice("Last Assault Instigator removed.", instigator)
            reset_database_value(bot, duelrecorduser, 'lastfullroomassult')
        elif settingchange == 'lastroman':
            reset_database_value(bot, duelrecorduser, 'lastfullroomcolosseuminstigator')
            bot.notice("Last Colosseum Instigator removed.", instigator)
            reset_database_value(bot, duelrecorduser, 'lastfullroomcolosseum')
        elif settingchange == 'lastinstigator':
            reset_database_value(bot, duelrecorduser, 'lastinstigator')
            bot.notice("Last Fought Instigator removed.", instigator)
        elif settingchange == 'halfhoursim':
            bot.notice("Simulating the half hour automated events.", instigator)
            halfhourtimer(bot)
        else:
            bot.notice("Must be an invalid command.", instigator)
    else:
        bot.notice(instigator + ", an admin command has not been written for the " + subcommand + " command.", instigator)

##########################
## 30 minute automation ##
##########################

@sopel.module.interval(1800)
def halfhourtimer(bot):
    now = time.time()

    ## Tier the stats
    tierratio = tierratio_level(bot)
    #healthregencurrent = tierratio * halfhour_regen_health_max
    magemanaregencurrent = tierratio * halfhour_regen_mage_mana_max


    ## Who gets to win a mysterypotion?
    randomuarray = []
    duelusersarray = get_database_value(bot, duelrecorduser, 'duelusers')

    ## Log Out Array
    logoutarray = []

    for u in bot.users:
        ## must have duels enabled, but has to use the game every so often
        if u in duelusersarray and u != bot.nick:

            ## Log out users that aren't playing
            lastcommandusedtime = get_timesince_duels(bot, u, 'lastcommand') or 0
            lastping = get_timesince_duels(bot, u, 'lastping') or 0
            if timeout_auto_opt_out < lastcommandusedtime and lastping < timeout_auto_opt_out:
                logoutarray.append(u)
                reset_database_value(bot, u, 'lastping')
            else:
                set_database_value(bot, u, 'lastping', now)

                uclass = get_database_value(bot, u, 'class_setting') or 'notclassy'
                mana = get_database_value(bot, u, 'magic_mana') or 0
                #health = get_database_value(bot, u, 'health_b4se') or 0

                ## Random user gets a mysterypotion
                lasttimedlootwinner = get_database_value(bot, duelrecorduser, 'lasttimedlootwinner') or bot.nick
                if u != lasttimedlootwinner:
                    randomuarray.append(u)

                ## award coin to all
                adjust_database_value(bot, u, 'loot_coin', halfhour_coin)

                ## health regenerates for all
                #if int(health) < healthregencurrent:
                    #adjust_database_value(bot, u, 'health_b4se', halfhour_regen_health)
                    #health = get_database_value(bot, u, 'health_b4se')
                    #if int(health) > healthregencurrent:
                        #set_database_value(bot, u, 'health_b4se', healthregencurrent)

                ## mages regen mana
                if uclass == 'mage':
                    if int(mana) < magemanaregencurrent:
                        adjust_database_value(bot, u, 'magic_mana', halfhour_regen_mage_mana)
                        mana = get_database_value(bot, u, 'magic_mana')
                        if int(mana) > magemanaregencurrent:
                            set_database_value(bot, u, 'magic_mana', magemanaregencurrent)

    ## Log Out Users
    adjust_database_array(bot, duelrecorduser, logoutarray, 'duelusers', 'del')

    ## Random winner select
    if randomuarray != []:
        lootwinner = halfhourpotionwinner(bot, randomuarray)
        loot_text = str(mysterypotiondispmsg + " Use .duel loot use mysterypotion to consume.")
        adjust_database_value(bot, lootwinner, 'mysterypotion', 1)
        lootwinnermsg = str(lootwinner + ' is awarded a mysterypotion ' + str(loot_text))
        bot.notice(lootwinnermsg, lootwinner)

#######################
## Valid Stats Array ##
#######################

def duels_valid_stats(bot):
    duelstatsadminarray = []
    for stattype in stats_admin_types:
        stattypeeval = eval("stats_"+stattype)
        for duelstat in stattypeeval:
            duelstatsadminarray.append(duelstat)
    return duelstatsadminarray

def array_compare(bot, indexitem, arraytoindex, arraytocompare):
    item = ''
    for x, y in zip(arraytoindex, arraytocompare):
        if x == indexitem:
            item = y
    return item
    
###########
## Tiers ##
###########

def tier_command(bot, command):
    tiercommandeval = 0
    for i in range(0,16):
        tiercheck = eval("commandarray_tier_unlocks_"+str(i))
        if command.lower() in tiercheck:
            tiercommandeval = int(i)
            continue
    return tiercommandeval

def tier_pepper(bot, pepper):
    tiernumber = commandarray_pepper_levels.index(pepper.lower())
    return tiernumber

def pepper_tier(bot, tiernumber):
    if not tiernumber:
        pepper = 'n00b'
    else:
        pepper = get_trigger_arg(commandarray_pepper_levels, tiernumber + 1)
        pepper = pepper.title()
    return pepper

def tier_xp(bot, xp):
    tiernumber = 0
    smallerxparray = []
    for x in commandarray_xp_levels:
        if x <= xp:
            smallerxparray.append(x)
    if smallerxparray != []:
        bigestxp = max(smallerxparray)
        tiernumber = commandarray_xp_levels.index(bigestxp)
    return tiernumber

#####################
## Target Criteria ##
#####################

## Target
def targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray):

    ## Guilty until proven Innocent
    validtarget = 0
    validtargetmsg = ''

    ## Null Target
    if not target:
        validtargetmsg = str(instigator + ", you must specify a target.")
        return validtarget, validtargetmsg

    ## Bot
    if target == bot.nick or target == 'duelrecorduser':
        validtargetmsg = str(instigator + ", " + target + " can't be targeted.")
        return validtarget, validtargetmsg

    ## Target can't be a valid command
    if target.lower() in commandarray_all_valid:
        validtargetmsg = str(instigator + ", " + target + "'s nick is the same as a valid command for duels.")
        return validtarget, validtargetmsg

    ## Target can't be duelrecorduser
    if target.lower() == duelrecorduser:
        validtargetmsg = str(instigator + ", " + target + "'s nick is unusable for duels.")
        return validtarget, validtargetmsg

    ## Offline User
    if target.lower() in [x.lower() for x in botvisibleusers] and target.lower() not in [y.lower() for y in currentuserlistarray]:
        target = actualname(bot, target)
        validtargetmsg = str(instigator + ", " + target + " is offline right now.")
        return validtarget, validtargetmsg

    ## Opted Out
    if target.lower() in [x.lower() for x in currentuserlistarray] and target.lower() not in [j.lower() for j in dueloptedinarray]:
        target = actualname(bot, target)
        validtargetmsg = str(instigator + ", " + target + " has duels disabled.")
        return validtarget, validtargetmsg

    ## None of the above
    if target.lower() not in [y.lower() for y in currentuserlistarray]:
        target = actualname(bot, target)
        validtargetmsg = str(instigator + ", " + target + " is either not here, or not a valid nick to target.")
        return validtarget, validtargetmsg

    validtarget = 1
    return validtarget, validtargetmsg

# mustpassthesetoduel
def duelcriteria(bot, usera, userb, currentduelplayersarray, inchannel):

    ## Guilty until proven Innocent
    validtarget = 0
    validtargetmsg = ''

    ## usera ignores lastfought
    useraclass = get_database_value(bot, usera, 'class_setting') or 'notclassy'
    if useraclass != 'knight':
        useralastfought = get_database_value(bot, usera, 'record_lastfought') or ''
    else:
        useralastfought = bot.nick

    ## Timeout Retrieval
    useratime = get_timesince_duels(bot, usera, 'timeout_timeout') or 0
    userbtime = get_timesince_duels(bot, userb, 'timeout_timeout') or 0
    channeltime = get_timesince_duels(bot, duelrecorduser, 'timeout_timeout') or 0

    ## Last instigator
    channellastinstigator = get_database_value(bot, duelrecorduser, 'lastinstigator') or bot.nick

    ## Current Users List
    dueluserslist = []
    for x in currentduelplayersarray:
        if x != bot.nick:
            dueluserslist.append(x)
    howmanyduelsers = len(dueluserslist)

    ## Correct userb Name
    userb = actualname(bot, userb)

    ## Devroom bypass
    devenabledchannels = get_database_value(bot, duelrecorduser, 'devenabled') or []
    if inchannel in devenabledchannels:
        validtarget = 1
        return validtarget, validtargetmsg

    ## Don't allow usera to duel twice in a row
    if usera == channellastinstigator and useratime <= INSTIGATORTIMEOUT:
        validtargetmsg = str("You may not instigate fights twice in a row within a half hour. You must wait for somebody else to instigate, or "+str(hours_minutes_seconds((INSTIGATORTIMEOUT - useratime)))+" .")
        return validtarget, validtargetmsg

    ## usera can't duel the same person twice in a row, unless there are only two people in the channel
    if userb == useralastfought and howmanyduelsers > 2:
        validtargetmsg = str(usera + ', You may not fight the same person twice in a row.')
        return validtarget, validtargetmsg

    ## usera Timeout
    if useratime <= USERTIMEOUT:
        validtargetmsg = str("You can't duel for "+str(hours_minutes_seconds((USERTIMEOUT - useratime)))+".")
        return validtarget, validtargetmsg

    ## Target Timeout
    if userbtime <= USERTIMEOUT:
        validtargetmsg = str(userb + " can't duel for "+str(hours_minutes_seconds((USERTIMEOUT - userbtime)))+".")
        return validtarget, validtargetmsg

    ## Channel Timeout
    if channeltime <= CHANTIMEOUT:
        validtargetmsg = str("Channel can't duel for "+str(hours_minutes_seconds((CHANTIMEOUT - channeltime)))+".")
        return validtarget, validtargetmsg

    validtarget = 1
    return validtarget, validtargetmsg

## Events
def eventchecks(bot, canduelarray, commandortarget, instigator, currentduelplayersarray, inchannel):

    ## Pass Go is no
    validtarget = 0
    validtargetmsg = ''

    if canduelarray == []:
        validtargetmsg = str(instigator + ", It looks like the full channel " + commandortarget + " event target finder has failed.")
        return validtarget, validtargetmsg

    ## Devroom bypass
    devenabledchannels = get_database_value(bot, duelrecorduser, 'devenabled') or []
    if inchannel in devenabledchannels:
       validtarget = 1
       return validtarget, validtargetmsg

    if instigator not in canduelarray:
        canduel, validtargetmsg = duelcriteria(bot, instigator, instigator, currentduelplayersarray, inchannel)
        return validtarget, validtargetmsg

    timeouteval = eval("timeout_"+commandortarget.lower())
    getlastusage = get_timesince_duels(bot, duelrecorduser, str('lastfullroom' + commandortarget)) or timeouteval
    getlastinstigator = get_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget + 'instigator')) or bot.nick

    if getlastusage < timeouteval:
        validtargetmsg = str(instigator + ", full channel " + commandortarget + " event can't be used for "+str(hours_minutes_seconds((timeouteval - getlastusage)))+".")
        return validtarget, validtargetmsg

    if getlastinstigator == instigator:
        validtargetmsg = str(instigator + ", You may not instigate a full channel " + commandortarget + " event twice in a row.")
        return validtarget, validtargetmsg

    validtarget = 1
    return validtarget, validtargetmsg

############
## Damage ##
############

def duels_damage(bot, damagescale, classwinner, classloser, winner, loser):

    ## Rogue can't be hurt by themselves or bot
    roguearraynodamage = [bot.nick,loser]
    if classloser == 'rogue' and winner in roguearraynodamage:
        damage = 0

    ## Bot deals a set amount
    elif winner == bot.nick:
        damage = bot_damage

    ## Barbarians get extra damage (minimum)
    elif classwinner == 'barbarian':
        damage = randint(duel_advantage_barbarian_min_damage, 120)

    ## vampires have a minimum damage
    elif classwinner == 'vampire' and winner != loser:
        damage = randint(0, duel_disadvantage_vampire_max_damage)

    ## All Other Players
    else:
        damage = randint(0, 120)

    ## Damage Tiers
    if damage > 0:
        damage = damagescale * damage

    return damage

def duels_damage_text(bot, damage, winnername, losername, bodypart, striketype, weapon, classwinner, bodypartname, winner, loser):

    if losername == winnername:
        losername = "themself"
    
    if damage == 0:
        damagetext = str(winnername + " " + striketype + " " + losername + " in the " + bodypartname + weapon + ', but deals no damage.')
    elif classwinner == 'vampire' and winner != loser:
        damagetext = str(winnername + " drains " + str(damage)+ " health from " + losername + weapon + " in the " + bodypartname + ".")
    else:
        damagetext = str(winnername + " " + striketype + " " + losername + " in the " + bodypartname + weapon + ", dealing " + str(damage) + " damage.")
    return damagetext

## Damage Resistance
def damage_resistance(bot, nick, damage, bodypart):
    damagetextarray = []

    ## Shields
    if damage > 0:
        shieldnick = get_database_value(bot, nick, 'magic_shield') or 0
        if shieldnick:
            damagemath = int(shieldnick) - damage
            if int(damagemath) > 0:
                adjust_database_value(bot, nick, 'magic_shield', -abs(damage))
                damage = 0
                absorbed = 'all'
            else:
                absorbed = damagemath + damage
                damage = abs(damagemath)
                reset_database_value(bot, nick, 'magic_shield')
            damagetextarray.append(nick + " absorbs " + str(absorbed) + " of the damage. ")

    ## Armor
    if damage > 0:
        armortype = array_compare(bot, "health_"+bodypart, stats_healthbodyparts, stats_armor)
        armornick = get_database_value(bot, nick, armortype) or 0
        if armornick:
            if "_" in armortype:
                armorname = armortype.split("_", 1)[1]
                armorname = armorname.replace("_", " ")
            else:
                armorname = armortype
            adjust_database_value(bot, nick, armortype, -1)
            damagepercent = randint(1, armor_relief_percentage) / 100
            damagereduced = damage * damagepercent
            damagereduced = int(damagereduced)
            damage = damage - damagereduced
            damagetext = str(nick + "s "+ armorname + " alleviated " + str(damagereduced) + " of the damage.")
            armornick = get_database_value(bot, nick, armortype) or 0
            if armornick <= 0:
                reset_database_value(bot, nick, armortype)
                damagetext = str(damagetext + ", causing the armor to break!")
            elif armornick <= 5:
                damagetext = str(damagetext + ", causing the armor to be in need of repair!")
            else:
                damagetext = str(damagetext + ".")
            damagetextarray.append(damagetext)

    return damage, damagetextarray

###################
## Living Status ##
###################

def whokilledwhom(bot, winner, loser):
    winnertextarray = []
    winnertextarray.append(loser + ' dies forcing a respawn!!')
    ## Reset mana and health
    reset_database_value(bot, loser, 'magic_mana')
    healthfresh(bot, loser) ## TODO, replace with just building the health
    ## update kills/deaths
    adjust_database_value(bot, winner, 'record_kills', 1)
    adjust_database_value(bot, loser, 'record_respawns', 1)
    ## Loot Corpse
    loserclass = get_database_value(bot, loser, 'class_setting') or 'notclassy'
    bountyonloser = get_database_value(bot, loser, 'bounty_amount')
    if bountyonloser:
        adjust_database_value(bot, winner, 'loot_coin', bountyonloser)
        reset_database_value(bot, loser, 'bounty_amount')
        winnertextarray.append(winner + " wins a bounty of " + str(bountyonloser) + " that was placed on " + loser + ".")
    ## rangers don't lose their stuff
    if loserclass != 'ranger':
        for x in potion_types:
            gethowmany = get_database_value(bot, loser, x)
            ## TODO array of loot won
            adjust_database_value(bot, winner, x, gethowmany)
            reset_database_value(bot, loser, x)
    return winnertextarray

def suicidekill(bot,loser):
    suicidetextarray = []
    suicidetextarray.append(loser + " committed suicide, forcing a respawn.")
    ## Reset mana
    reset_database_value(bot, loser, 'magic_mana')
    suicidetextarray.append(loser + " lose all mana.")
    ## Stock health
    #set_database_value(bot, loser, 'health_b4se', stockhealth)
    healthfresh(bot, loser) ## TODO: non-tiered
    ## update deaths
    adjust_database_value(bot, loser, 'record_respawns', 1)
    ## bounty
    bountyonloser = get_database_value(bot, loser, 'bounty_amount')
    if bountyonloser:
        suicidetextarray.append(loser + " wastes the bounty of " + str(bountyonloser) + " coin.")
    reset_database_value(bot, loser, 'bounty_amount')
    ## rangers don't lose their stuff
    loserclass = get_database_value(bot, loser, 'class_setting') or 'notclassy'
    if loserclass != 'ranger':
        for x in potion_types:
            reset_database_value(bot, loser, x)
        suicidetextarray.append(loser + " loses all loot.")
    return suicidetextarray

def healthcheck(bot, nick):
    ## logic for crippled bodyparts
    for part in stats_healthbodyparts:
        currenthealthtier = tierratio_level(bot)
        maxhealthpart = array_compare(bot, part, stats_healthbodyparts, health_bodypart_max)
        maxhealthpart = int(maxhealthpart)
        currenthealthtier = currenthealthtier * int(maxhealthpart)
        currenthealthtier = int(currenthealthtier)
        gethowmany = get_database_value(bot, nick, part) or 0
        if not gethowmany or gethowmany <= 0 or gethowmany > currenthealthtier:
            set_database_value(bot, nick, part, currenthealthtier)
    ## no mana at respawn
    mana = get_database_value(bot, nick, 'magic_mana')
    if int(mana) <= 0:
        reset_database_value(bot, nick, 'magic_mana')

def healthfresh(bot, nick):
    ## logic for crippled bodyparts
    for part in stats_healthbodyparts:
        currenthealthtier = tierratio_level(bot)
        maxhealthpart = array_compare(bot, part, stats_healthbodyparts, health_bodypart_max)
        maxhealthpart = int(maxhealthpart)
        currenthealthtier = currenthealthtier * int(maxhealthpart)
        currenthealthtier = int(currenthealthtier)
        gethowmany = get_database_value(bot, nick, part) or 0
        set_database_value(bot, nick, part, currenthealthtier)
    ## no mana at respawn
    mana = get_database_value(bot, nick, 'magic_mana')
    if int(mana) <= 0:
        reset_database_value(bot, nick, 'magic_mana')

## health
def get_health(bot,nick):
    totalhealth = 0
    for x in stats_healthbodyparts:
        gethowmany = get_database_value(bot, nick, x)
        if gethowmany:
            totalhealth = totalhealth + gethowmany
    return totalhealth

def bodypartarray(bot, nick):
    currentbodypartsarray = []
    for x in stats_healthbodyparts:
        gethowmany = get_database_value(bot, nick, x)
        if gethowmany:
            currentbodypartsarray.append(x)
    return currentbodypartsarray

######################
## On Screen Text ##
######################

def onscreentext(bot, texttargetarray, textarraycomplete):
    combinedtextarray = []
    currentstring = ''
    for textstring in textarraycomplete:
        if currentstring == '':
            currentstring = textstring
        else:
            tempstring = str(currentstring + "   " + textstring)
            if len(tempstring) <= 200:
                currentstring = tempstring
            else:
                combinedtextarray.append(currentstring)
                currentstring = textstring
    if currentstring != '':
        combinedtextarray.append(currentstring)
    for combinedline in combinedtextarray:
        for user in texttargetarray:
            if user == 'say':
                bot.say(combinedline)
            elif user.startswith("#"):
                bot.msg(user, combinedline)
            else:
                bot.notice(combinedline, user)

################
## DUEL Names ##
################

def duel_names(bot, nick, channel):
    nickname = ''
    for q in duel_nick_order:
        nickscriptdef = str(q + "(bot, nick, channel)")
        nicknameadd = eval(nickscriptdef)
        if nicknameadd != '':
            if nickname != '':
                nickname = str(nickname + " " + nicknameadd)
            else:
                nickname = nicknameadd
    if nickname == '':
        nickname = nick
    return nickname

def nicktitles(bot, nick, channel):
    nickname = actualname(bot,nick)
    ## custom title
    nicktitle = get_database_value(bot, nick, 'title')
    ## bot.owner
    try:
        if nicktitle:
            nickname = str(nicktitle+" " + nickname)
        elif nick.lower() in bot.config.core.owner.lower():
            nickname = str("The Legendary " + nickname)
    ## development_team
        elif nick in development_team:
            nickname = str("The Extraordinary " + nickname)
    ## OP
        elif bot.privileges[channel.lower()][nick.lower()] == OP:
            nickname = str("The Magnificent " + nickname)
    ## VOICE
        elif bot.privileges[channel.lower()][nick.lower()] == VOICE:
            nickname = str("The Incredible " + nickname)
    ## bot.admin
        elif nick in bot.config.core.admins:
            nickname = str("The Spectacular " + nickname)
    ## else
        else:
            nickname = str(nickname)
    except KeyError:
        nickname = str(nickname)
    return nickname

def nickpepper(bot, nick, channel):
    pepperstart = get_pepper(bot, nick)
    if not pepperstart or pepperstart == '':
        nickname = "(n00b)"
    else:
        nickname = str("(" + pepperstart.title() + ")")
    return nickname

def nickmagicattributes(bot, nick, channel):
    nickname = ''
    nickcurse = get_database_value(bot, nick, 'magic_curse')
    nickshield = get_database_value(bot, nick, 'magic_shield')
    magicattrarray = []
    if nickcurse:
        magicattrarray.append("[Cursed]")
    if nickshield:
        magicattrarray.append("[Shielded]")
    if nickname != []:
        for x in magicattrarray:
            if nickname != '':
                nickname = str(nickname + x)
            else:
                nickname = x
    return nickname

def nickarmor(bot, nick, channel):
    nickname = ''
    for x in stats_armor:
        gethowmany = get_database_value(bot, nick, x)
        if gethowmany:
            nickname = "{Armored}"
    return nickname

def actualname(bot,nick):
    actualnick = nick
    for u in bot.users:
        if u.lower() == nick.lower():
            actualnick = u
    return actualnick

##################
## Pepper level ##
##################

def get_pepper(bot, nick):
    if nick == bot.nick:
        pepper = 'Dragon Breath Chilli'
        return pepper
    xp = get_database_value(bot, nick, 'record_xp') or 0
    if not xp:
        pepper = 'n00b'
        return pepper
    xptier = tier_xp(bot, xp)
    pepper = pepper_tier(bot, xptier)
    # advance respawn tier
    tiernumber = tier_pepper(bot, pepper)
    currenttier = get_database_value(bot, duelrecorduser, 'leveling_tier') or 0
    if tiernumber > currenttier:
        set_database_value(bot, duelrecorduser, 'leveling_tier', tiernumber)
    nicktier = get_database_value(bot, nick, 'leveling_tier')
    if tiernumber != nicktier:
        set_database_value(bot, nick, 'leveling_tier', tiernumber)
    pepper = pepper.title()
    return pepper

##########
## Time ##
##########

def get_timesince_duels(bot, nick, databasekey):
    now = time.time()
    last = get_database_value(bot, nick, databasekey)
    return abs(now - int(last))

def get_timeout_timeout(bot, nick):
    time_since = get_timesince_duels(bot, nick, 'timeout_timeout')
    if time_since < USERTIMEOUT:
        timediff = str(hours_minutes_seconds((USERTIMEOUT - time_since)))
    else:
        timediff = 0
    return timediff

def hours_minutes_seconds(countdownseconds):
    time = float(countdownseconds)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minute = time // 60
    time %= 60
    second = time
    displaymsg = ''
    timearray = ['hour','minute','second']
    for x in timearray:
        currenttimevar = eval(x)
        if currenttimevar >= 1:
            timetype = x
            if currenttimevar > 1:
                timetype = str(x+"s")
            displaymsg = str(displaymsg + str(int(currenttimevar)) + " " + timetype + " ")
    return displaymsg

#############
## Streaks ##
#############

def set_current_streaks(bot, nick, winlose):
    if winlose == 'win':
        beststreaktype = 'streak_win_best'
        currentstreaktype = 'streak_win_current'
        oppositestreaktype = 'streak_loss_current'
    elif winlose == 'loss':
        beststreaktype = 'streak_loss_best'
        currentstreaktype = 'streak_loss_current'
        oppositestreaktype = 'streak_win_current'

    ## Update Current streak
    adjust_database_value(bot, nick, currentstreaktype, 1)
    set_database_value(bot, nick, 'streak_type_current', winlose)

    ## Update Best Streak
    beststreak = get_database_value(bot, nick, beststreaktype) or 0
    currentstreak = get_database_value(bot, nick, currentstreaktype) or 0
    if int(currentstreak) > int(beststreak):
        set_database_value(bot, nick, beststreaktype, int(currentstreak))

    ## Clear current opposite streak
    reset_database_value(bot, nick, oppositestreaktype)

def get_current_streaks(bot, winner, loser):
    winner_loss_streak = get_database_value(bot, winner, 'streak_loss_current') or 0
    loser_win_streak = get_database_value(bot, loser, 'streak_win_current') or 0
    return winner_loss_streak, loser_win_streak

def get_streaktext(bot, winner, loser, winner_loss_streak, loser_win_streak):
    win_streak = get_database_value(bot, winner, 'streak_win_current') or 0
    streak = ' (Streak: %d)' % win_streak if win_streak > 1 else ''
    broken_streak = ', recovering from a streak of %d losses' % winner_loss_streak if winner_loss_streak > 1 else ''
    broken_streak += ', ending %s\'s streak of %d wins' % (loser, loser_win_streak) if loser_win_streak > 1 else ''
    if broken_streak:
        streaktext = str("%s wins%s!%s" % (winner, broken_streak, streak))
    else:
        streaktext = ''
    return streaktext

###############
## Inventory ##
###############

def randominventory(bot, instigator):
    yourclass = get_database_value(bot, instigator, 'class_setting') or 'notclassy'
    if yourclass == 'scavenger':
        randomfindchance = randint(duel_advantage_scavenger_loot_find, 100)
    else:
        randomfindchance = randint(0, 120)
    randominventoryfind = 'false'
    if randomfindchance >= 90:
        randominventoryfind = 'true'
    return randominventoryfind

def halfhourpotionwinner(bot, randomuarray):
    winnerselectarray = []
    recentwinnersarray = get_database_value(bot, duelrecorduser, 'lasttimedlootwinners') or []
    lasttimedlootwinner = get_database_value(bot, duelrecorduser, 'lasttimedlootwinner') or bot.nick
    howmanyusers = len(randomuarray)
    if not howmanyusers > 1:
        reset_database_value(bot, duelrecorduser, 'lasttimedlootwinner')
    for x in randomuarray:
        if x not in recentwinnersarray and x != lasttimedlootwinner:
            winnerselectarray.append(x)
    if winnerselectarray == [] and randomuarray != []:
        reset_database_value(bot, duelrecorduser, 'lasttimedlootwinners')
        return halfhourpotionwinner(bot, randomuarray)
    lootwinner = get_trigger_arg(winnerselectarray, 'random') or bot.nick
    adjust_database_array(bot, duelrecorduser, [lootwinner], 'lasttimedlootwinners', 'add')
    set_database_value(bot, duelrecorduser, 'lasttimedlootwinner', lootwinner)
    return lootwinner

######################
## Weapon Selection ##
######################

## allchan weapons
def getallchanweaponsrandom(bot):
    allchanweaponsarray = []
    for u in bot.users:
        weaponslist = get_database_value(bot, u, 'weaponslocker_complete') or ['fist']
        for x in weaponslist:
            allchanweaponsarray.append(x)
    weapon = get_trigger_arg(allchanweaponsarray, 'random')
    return weapon

def weaponofchoice(bot, nick):
    weaponslistselect = []
    weaponslist = get_database_value(bot, nick, 'weaponslocker_complete') or []
    lastusedweaponarry = get_database_value(bot, nick, 'weaponslocker_lastweaponusedarray') or []
    lastusedweapon = get_database_value(bot, nick, 'weaponslocker_lastweaponused') or 'fist'
    howmanyweapons = get_database_array_total(bot, nick, 'weaponslocker_complete') or 0
    if not howmanyweapons > 1:
        reset_database_value(bot, nick, 'weaponslocker_lastweaponused')
    for x in weaponslist:
        if len(x) > weapon_name_length:
            adjust_database_array(bot, nick, [x], 'weaponslocker_complete', 'del')
        if x not in lastusedweaponarry and x != lastusedweapon and len(x) <= weapon_name_length:
            weaponslistselect.append(x)
    if weaponslistselect == [] and weaponslist != []:
        reset_database_value(bot, nick, 'weaponslocker_lastweaponusedarray')
        return weaponofchoice(bot, nick)
    weapon = get_trigger_arg(weaponslistselect, 'random') or 'fist'
    adjust_database_array(bot, nick, [weapon], 'weaponslocker_lastweaponusedarray', 'add')
    set_database_value(bot, nick, 'weaponslocker_lastweaponused', weapon)
    return weapon

def weaponformatter(bot, weapon):
    if weapon == '':
        weapon = weapon
    elif weapon.lower().startswith(('a ', 'an ', 'the ')):
        weapon = str('with ' + weapon)
    elif weapon.split(' ', 1)[0].endswith("'s"):
        weapon = str('with ' + weapon)
    elif weapon.lower().startswith(('a', 'e', 'i', 'o', 'u')):
        weapon = str('with an ' + weapon)
    elif weapon.lower().startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
        if weapon.endswith('s'):
            weapon = str("with " + weapon)
        else:
            weapon = str("with " + weapon + "s")
    elif weapon.lower().startswith('with'):
        weapon = str(weapon)
    else:
        weapon = str('with a ' + weapon)
    return weapon

################
## Stat Reset ##
################

def statreset(bot, nick): ## TODO update
    now = time.time()
    getlastchanstatreset = get_database_value(bot, duelrecorduser, 'chanstatsreset')
    if not getlastchanstatreset:
        set_database_value(bot, duelrecorduser, 'chanstatsreset', now)
    getnicklastreset = get_database_value(bot, nick, 'chanstatsreset')
    if getnicklastreset < getlastchanstatreset:
        duelstatsadminarray = duels_valid_stats(bot)
        for x in duelstatsadminarray:
            reset_database_value(bot, nick, x)
        set_database_value(bot, nick, 'chanstatsreset', now)

################
## Tier ratio ##
################

def tierratio_level(bot):
    currenttier = get_database_value(bot, duelrecorduser, 'leveling_tier') or 1
    tierratio = get_trigger_arg(commandarray_tier_ratio, currenttier) or 1
    return tierratio

###################
## Select Winner ##
###################

def selectwinner(bot, nickarray):
    statcheckarray = ['health','record_xp','record_kills','record_respawns','streak_win_current']

    ## empty var to start
    for user in nickarray:
        reset_database_value(bot, user, 'winnerselection')

    ## everyone gets a roll
    for user in nickarray:
        adjust_database_value(bot, user, 'winnerselection', 1)

    ## random roll
    randomrollwinner = get_trigger_arg(nickarray, 'random')
    adjust_database_value(bot, randomrollwinner, 'winnerselection', 1)

    ## Stats
    for x in statcheckarray:
        statscore = 0
        if x == 'record_respawns' or x == 'streak_win_current':
            statscore = 99999999
        statleader = ''
        for u in nickarray:
            if x != 'health':
                value = get_database_value(bot, u, x) or 0
            else:
                scriptdef = str('get_' + x + '(bot,u)')
                value = eval(scriptdef)
            if x == 'record_respawns' or x == 'streak_win_current':
                if int(value) < statscore:
                    statleader = u
                    statscore = int(value)
            else:
                if int(value) > statscore:
                    statleader = u
                    statscore = int(value)
        adjust_database_value(bot, statleader, 'winnerselection', 1)

    ## weaponslocker not empty
    for user in nickarray:
        weaponslist = get_database_value(bot, user, 'weaponslocker_complete') or []
        if weaponslist != []:
            adjust_database_value(bot, user, 'winnerselection', 1)

    ## anybody rogue?
    for user in nickarray:
        nickclass = get_database_value(bot, user, 'class_setting') or ''
        if nickclass == 'rogue':
            adjust_database_value(bot, user, 'winnerselection', 1)

    ## Dice rolling occurs now
    for user in nickarray:
        rolls = get_database_value(bot, user, 'winnerselection') or 0
        maxroll = winnerdicerolling(bot, user, rolls)
        set_database_value(bot, user, 'winnerselection', maxroll)

    ## curse check
    for user in nickarray:
        cursed = get_database_value(bot, user, 'magic_curse') or 0
        if cursed:
            reset_database_value(bot, user, 'winnerselection')
            adjust_database_value(bot, user, 'magic_curse', -1)

    ## who wins
    winnermax = 0
    winner = ''
    for u in nickarray:
        maxstat = get_database_value(bot, u, 'winnerselection') or 0
        if int(maxstat) > winnermax:
            winner = u
            winnermax = maxstat

    ## Clear value
    for user in nickarray:
        reset_database_value(bot, user, 'winnerselection')

    if not winner:
        for u in nickarray:
            maxroll = winnerdicerolling(bot, u, 2)
            set_database_value(bot, u, 'winnerselection', maxroll)
        winnermax = 0
        winner = ''
        for u in nickarray:
            maxstat = get_database_value(bot, u, 'winnerselection') or 0
            if int(maxstat) > winnermax:
                winner = u
                winnermax = maxstat

    return winner

def winnerdicerolling(bot, nick, rolls):
    nickclass = get_database_value(bot, nick, 'class_setting') or ''
    rolla = 0
    rollb = 20
    if nickclass == 'rogue':
        rolla = 8
    fightarray = []
    while int(rolls) > 0:
        fightroll = randint(rolla, rollb)
        fightarray.append(fightroll)
        rolls = int(rolls) - 1
    try:
        fight = max(fightarray)
    except ValueError:
        fight = 0
    return fight

#####################
## Magic attributes ##
######################

def get_current_magic_attributes(bot, nick):
    nickshield = get_database_value(bot, nick, 'magic_shield') or 0
    nickcurse = get_database_value(bot, nick, 'magic_curse') or 0
    return nickshield, nickcurse

def get_magic_attributes_text(bot, winner, loser, winnershieldstart, losershieldstart, winnercursestart, losercursestart):
    attributetext = []
    winnershieldnow, winnercursenow = get_current_magic_attributes(bot, winner)
    losershieldnow, losercursenow = get_current_magic_attributes(bot, loser)
    magicattributesarray = ['magic_shield','magic_curse']
    nickarray = ['winner','loser']
    attributetext = ''
    for j in nickarray:
        if j == 'winner':
            scanningperson = winner
        else:
            scanningperson = loser
        for x in magicattributesarray:
            magicname = x.replace("magic_", "")
            workingvarnow = eval(j+magicname+"now")
            workingvarstart = eval(j+magicname+"start")
            if workingvarnow == 0 and workingvarnow != workingvarstart:
                attributetext.append(scanningperson + " is no longer affected by " + x + ".")
    return attributetext

###############
## ScoreCard ##
###############

def get_winlossratio(bot,target):
    wins = get_database_value(bot, target, 'record_wins')
    wins = int(wins)
    losses = get_database_value(bot, target, 'record_losses')
    losses = int(losses)
    if not losses:
        if not wins:
            winlossratio = 0
        else:
            winlossratio = wins
    elif not wins:
        if not losses:
            winlossratio = 0
        else:
            winlossratio = int(losses) * -1
    else:
        winlossratio = float(wins)/losses
    return winlossratio

##############
## Database ##
##############

def get_database_value(bot, nick, databasekey):
    databasecolumn = str('duels_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('duels_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)

def reset_database_value(bot, nick, databasekey):
    databasecolumn = str('duels_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, None)

def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey) or 0
    databasecolumn = str('duels_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))

def get_database_array_total(bot, nick, databasekey):
    array = get_database_value(bot, nick, databasekey) or []
    entriestotal = len(array)
    return entriestotal

def adjust_database_array(bot, nick, entries, databasekey, adjustmentdirection):
    adjustarray = get_database_value(bot, nick, databasekey) or []
    adjustarraynew = []
    for x in adjustarray:
        adjustarraynew.append(x)
    reset_database_value(bot, nick, databasekey)
    adjustarray = []
    if adjustmentdirection == 'add':
        for y in entries:
            if y not in adjustarraynew:
                adjustarraynew.append(y)
    elif adjustmentdirection == 'del':
        for y in entries:
            if y in adjustarraynew:
                adjustarraynew.remove(y)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        reset_database_value(bot, nick, databasekey)
    else:
        set_database_value(bot, nick, databasekey, adjustarray)

##########
## ARGS ##
##########

def get_trigger_arg(triggerargsarray, number):
    ## Create
    if number == 'create':
        triggerargsarraynew = []
        if triggerargsarray:
            for word in triggerargsarray.split():
                triggerargsarraynew.append(word)
        return triggerargsarraynew
    totalarray = len(triggerargsarray)
    totalarray = totalarray + 1
    triggerarg = ''
    ## Comma Seperated List
    if number == 'list':
        for x in triggerargsarray:
            if triggerarg != '':
                triggerarg  = str(triggerarg  + ", " + x)
            else:
                triggerarg  = str(x)
        return triggerarg
    ## Random Entry from array
    if number == 'random':
        if triggerargsarray == []:
            return triggerarg
        temparray = []
        for d in triggerargsarray:
            temparray.append(d)
        shuffledarray = random.shuffle(temparray)
        randomselected = random.randint(0,len(temparray) - 1)
        triggerarg = str(temparray [randomselected])
        return triggerarg
    ## Last
    if number == 'last':
        if totalarray > 1:
            totalarray = totalarray -2
            triggerarg = str(triggerargsarray[totalarray])
        return triggerarg
    ## Complete
    if number == 0:
        for x in triggerargsarray:
            if triggerarg != '':
                triggerarg = str(triggerarg + " " + str(x))
            else:
                triggerarg = str(x)
        return triggerarg
    ## Other
    if "^" in str(number) or number == 0 or str(number).endswith("+") or str(number).endswith("-") or str(number).endswith("<") or str(number).endswith(">"):
        if str(number).endswith("+"):
            rangea = re.sub(r"\+", '', str(number))
            rangea = int(rangea)
            rangeb = totalarray
        elif str(number).endswith("-"):
            rangea = 1
            rangeb = re.sub(r"-", '', str(number))
            rangeb = int(rangeb) + 1
        elif str(number).endswith(">"):
            rangea = re.sub(r">", '', str(number))
            rangea = int(rangea) + 1
            rangeb = totalarray
        elif str(number).endswith("<"):
            rangea = 1
            rangeb = re.sub(r"<", '', str(number))
            rangeb = int(rangeb)
        elif "^" in str(number):
            rangea = number.split("^", 1)[0]
            rangeb = number.split("^", 1)[1]
            rangea = int(rangea)
            rangeb = int(rangeb) + 1
        if rangea <= totalarray:
            for i in range(rangea,rangeb):
                arg = get_trigger_arg(triggerargsarray, i)
                if triggerarg != '':
                    triggerarg = str(triggerarg + " " + arg)
                else:
                    triggerarg = str(arg)
    elif str(number).endswith("!"):
        number = re.sub(r"!", '', str(number))
        for i in range(1,totalarray):
            if int(i) != int(number):
                arg = get_trigger_arg(triggerargsarray, i)
                if triggerarg != '':
                    triggerarg = str(triggerarg + " " + arg)
                else:
                    triggerarg = str(arg)
    else:
        number = int(number) - 1
        try:
            triggerarg = triggerargsarray[number]
        except IndexError:
            triggerarg = ''
    return triggerarg
