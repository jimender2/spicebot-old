#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
from sopel.module import commands, nickname_commands, rule, priority, example
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
from difflib import SequenceMatcher
from more_itertools import sort_together
from operator import itemgetter
import requests
from fake_useragent import UserAgent
from lxml import html
from statistics import mean
import itertools

moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from DuelClassic import *

###################
## Configurables ##
###################

###########
## Tiers ##
###########

class duels_tier(object):
    xp = [0,1,100,250,500,1000,2500,5000,7500,10000,15000,25000,45000,70000,100000,250000] ## XP
    ratio = [1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.1,2.2,2.3,2.4,2.5] ## Tier Ratios
    pepper = ['n00b','pimiento','sonora','anaheim','poblano','jalapeno','serrano','chipotle','tabasco','cayenne','thai pepper','datil','habanero','ghost chili','mace','pure capsaicin'] ## Pepper Levels
    def __init__(self, x):
        self.x = x

#######################################
## Character Creation and Base Stats ##
#######################################

class duels_character(object):
    class setup(object):
        class required(object):
            def __init__(self, y):
                self.z = ['Class','race','gender']
        def __init__(self, y):
            self.y = y
        class valid(object):
            Class = ['blacksmith','mage','scavenger','rogue','ranger','knight','paladin']
            gender = ['male','female']
            race = ['human','barbarian','fiend','vampire']
            def __init__(self, y):
                self.z = z
    def __init__(self, x):
        self.x = x

## Character creation basics
duels_character_setup = ['Class','race','gender']

## Valid settings
duels_character_setup_valid_Class = ['blacksmith','mage','scavenger','rogue','ranger','knight','paladin']
duels_character_setup_valid_gender = ['male','female']
duels_character_setup_valid_race = ['human','barbarian','fiend','vampire']

## Classes SPECIAL
duels_character_special_Class_blacksmith = [5,5,5,5,5,5,5]
duels_character_special_Class_mage = [5,5,5,5,5,5,5]
duels_character_special_Class_scavenger = [5,5,5,5,5,5,5]
duels_character_special_Class_rogue = [5,5,5,5,5,5,5]
duels_character_special_Class_ranger = [5,5,5,5,5,5,5]
duels_character_special_Class_knight = [5,5,5,5,5,5,5]
duels_character_special_Class_paladin = [5,5,5,5,5,5,5]

## races SPECIAL
duels_character_special_race_human = [5,5,5,5,5,5,5]
duels_character_special_race_barbarian = [5,5,5,5,5,5,5]
duels_character_special_race_fiend = [5,5,5,5,5,5,5]
duels_character_special_race_vampire = [5,5,5,5,5,5,5]





################################
## Command Structure Settings ##
################################

## NOTE: Command creation Checklist
##
## * Command Tier
## * Stamina Required

## Commands that must be run in channel and not in privmsg
duels_commands_inchannel  = ['roulette','assault','colosseum','bounty','hungergames','devmode','quest','deathblow','combat','grenade','Classic']

## Commands that can only be run by bot.admin
duels_commands_admin = ['admin','devmode','game']

### Command Tiers
duels_commands_tier_self_use = ['stats', 'loot', 'streaks','health','character']
duels_commands_tier_unlocks_0 = ['game', 'docs', 'admin', 'author', 'on', 'off','devmode','version','deathblow','combat','grenade','Classic','setup']
duels_commands_tier_unlocks_1 = ['tier','usage']
duels_commands_tier_unlocks_2 = ['streaks', 'bounty', 'harakiri']
duels_commands_tier_unlocks_3 = ['weaponslocker']
duels_commands_tier_unlocks_4 = ['leaderboard', 'warroom']
duels_commands_tier_unlocks_5 = ['stats', 'loot','health','character']
duels_commands_tier_unlocks_6 = ['magic', 'armor']
duels_commands_tier_unlocks_7 = ['assault']
duels_commands_tier_unlocks_8 = ['roulette','monster']
duels_commands_tier_unlocks_9 = ['random']
duels_commands_tier_unlocks_10 = ['colosseum']
duels_commands_tier_unlocks_11 = ['title']
duels_commands_tier_unlocks_12 = ['mayhem']
duels_commands_tier_unlocks_13 = ['hungergames']
duels_commands_tier_unlocks_14 = ['quest']
duels_commands_tier_unlocks_15 = []

## Stamina Requirements for Commands
duels_commands_stamina_free = ['on','off','admin','devmode','game','stats','loot','streaks','health','tier','docs','author','version','usage','streaks','bounty','weaponslocker','armor','title','leaderboard', 'warroom','grenade','character','setup']
duels_commands_stamina_combat = 5
duels_commands_stamina_deathblow = 1
duels_commands_stamina_Classic = 1
duels_commands_stamina_harakiri = 1
duels_commands_stamina_magic = 2
duels_commands_stamina_monster = 10
duels_commands_stamina_assault = 10
duels_commands_stamina_roulette = 2
duels_commands_stamina_random = 3
duels_commands_stamina_colosseum = 20
duels_commands_stamina_mayhem = 25
duels_commands_stamina_hungergames = 20
duels_commands_stamina_quest = 30

## Alternative Commands
duels_commands_alternate_list = ['on','off','random','assault','author','docs','loot','admin','Classic','weaponslocker','character'] ## Main Commands that have alternates
duels_commands_alternate_on = ['enable','activate']
duels_commands_alternate_off = ['disable','deactivate']
duels_commands_alternate_random = ['anyone','somebody','available','someone']
duels_commands_alternate_assault = ['everyone','everybody','channel']
duels_commands_alternate_author = ['credit']
duels_commands_alternate_loot = ['backpack']
duels_commands_alternate_weaponslocker = ['weapons']
duels_commands_alternate_admin = ['-a']
duels_commands_alternate_Classic = ['retro']
duels_commands_alternate_docs = ['help','man']
duels_commands_alternate_character = ['char']

## Command Checks
duels_commands_canduel_generate = ['mayhem','hungergames','monster','random']
duels_commands_canduel_remove_bot = ['mayhem','hungergames','colosseum','assault','quest','warroom','grenade']
duels_commands_events = ['mayhem','hungergames','colosseum','assault','quest']
duels_commands_special_events = ['combat','roulette','assault','roulette','monster','random','colosseum','mayhem','hungergames','quest']


############################################################################################################################################################################################################################
############################################################################################################################################################################################################################



#########################
## Version Information ##
#########################

duels_version_plain = '1.5.17' ## If the online check fails
duels_version_github_page = "https://github.com/deathbybandaid/SpiceBot/commits/master/modules/Games/Duels.py"
duels_version_github_xpath = '//*[@id="js-repo-pjax-container"]/div[2]/div[1]/div[2]/div[1]/text()'










## more stuff
bodyparts_required = ['torso','head']

## Admin Stats Cycling
stats_admin_types = ['healthbodyparts','armor','loot','record','magic','streak','timeout','title','bounty','weaponslocker','leveling','other','stamina','character','character_start','character_initial']
## Health Stats
stats_healthbodyparts = ['head','torso','left_arm','right_arm','left_leg','right_leg','junk']
## Armor Stats
stats_armor = ['helmet','breastplate','left_gauntlet','right_gauntlet','left_greave','right_greave','codpiece']
## Loot Stats
stats_loot = ['magicpotion','healthpotion','mysterypotion','timepotion','staminapotion','poisonpotion','manapotion','grenade','coin','stimpack']
## character stats
stats_character_initial = ['Class','race','gender']
stats_character_start = ['charactercreated','charactercreatedb']
stats_character = ['strength', 'perception', 'endurance', 'charisma', 'intelligence', 'agility', 'luck']
## Record Stats
stats_record = ['wins','losses','xp','respawns','kills','lastfought']
## Streak Stats
stats_streak = ['streak_loss_current','streak_win_current','streak_type_current','streak_win_best','streak_loss_best']
## Magic Stats
stats_magic = ['mana','curse','shield']
## Timeout Stats
stats_timeout = ['timeout_opttime','timeout_timeout']
## Title Stats
stats_title = ['title_setting']
## Bounty Stats
stats_bounty = ['bounty']
## Stamina
stats_stamina = ['stamina']
## Weaponslocker Stats
stats_weaponslocker = ['weaponslocker_complete','weaponslocker_lastweaponusedarray','weaponslocker_lastweaponused']
## Leveling Stats
stats_leveling = ['tier']
## Other
stats_other = ['chanstatsreset']




## Documentation and Development
GITWIKIURL = "https://github.com/deathbybandaid/SpiceBot/wiki/Duels" ## Wiki URL, change if not using with spicebot
development_team = ['deathbybandaid','Mace_Whatdo','dysonparkes','under_score'] ## Dev Team

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

## Quest
timeout_quest = 1800 ## Time Between Full Channel Quests

## Colosseum
timeout_colosseum = 1800 ## Time Between colosseum events

## hungergames
timeout_hungergames = 1800

## mayhem
timeout_mayhem = 1800

## Random Target
random_payout = 100

## Class
duels_valid_Class = ['blacksmith','barbarian','mage','scavenger','rogue','ranger','fiend','vampire','knight','paladin'] ## Valid Classes

## Title
title_cost = 100 ## ## how many coin to change title

## Bug Bounty
bugbounty_reward = 100 ## users that find a bug in the code, get a reward

## Loot
loot_view = ['coin','grenade','healthpotion','manapotion','poisonpotion','timepotion','staminapotion','mysterypotion','magicpotion','stimpack'] ## how to organize backpack
potion_types = ['healthpotion','manapotion','poisonpotion','timepotion','staminapotion','mysterypotion','magicpotion'] ## types of potions
loot_winnable = ['healthpotion','manapotion','poisonpotion','timepotion','staminapotion','mysterypotion','magicpotion']
loot_all_types = ['healthpotion','manapotion','poisonpotion','timepotion','staminapotion','mysterypotion','magicpotion','stimpack','grenade']
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
timepotiontimeoutarray = ['timeout_timeout','lastfullroomcolosseum','lastfullroomassult','timeout_opttime']
## stamina potion
staminapotion_worth = 15 ##normal stamina potion worth
staminapotiondispmsg = str(": worth " + str(staminapotion_worth) + " stamina.")
## Magic Potions
magicpotiondispmsg = str(": Not consumable, sellable, or purchasable. Trade this for the potion you want!")
## stimpacks
stimpack_worth = 100
stimpack_worth_barbarian = 125 ## stimpack worth for barbarians
stimpackdispmsg = str(": Worth "+str(stimpack_worth)+" health to a specific bodypart. Apply directly wear it hurts!!")

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
armor_repair_cost = .5
armor_cost_blacksmith_cut = .8
armor_sell_blacksmith_cut = 1.5
armor_durability = 10
armor_durability_blacksmith = 15
armor_relief_percentage = 33 ## has to be converted to decimal later
health_bodypart_max = [330,1000,250,250,500,500,40]

## Stamina
staminamax = 60

title_cost = 100


## Bodypart damage modifiers
## TODO

## Half Hour Timer
timeout_auto_opt_out = 259200 ## Opt out users after 3 days of inactivity
halfhour_regen_health, halfhour_regen_health_max = 50,500 ## health regen rate
halfhour_regen_mage_mana, halfhour_regen_mage_mana_max = 50, 500 ## mages regenerate mana: rate
halfhour_coin = 15 ## coin gain per half hour

## Main Duel Runs
duel_combat_timeouts = 'false'
stat_check_commands_list = ['author','version','docs','on','off','game','devmode','admin']
duel_lockout_timer = 300
duels_combat_lockout_list = ['combat','mayhem','assault','quest','random','monster']
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
target_ignore_list = ['spicebot','spiceduels']
duelrecorduser = 'duelrecorduser'
stat_admin_commands = ['set','reset','view'] ## valid admin subcommands
stats_view = ['Class','curse','stamina','shield','mana','xp','wins','losses','winlossratio','respawns','kills','lastfought','bounty','timeout_timeout']
stats_view_functions = ['winlossratio','timeout_timeout'] ## stats that use their own functions to get a value

## array of insulting departures
cowardarray = ["What a coward!","What a Woosy!","Run away, loser!","Shame on you!","Scaredy-cat!"]

## Built-in docs
helpdocs_basic_Classic = "shows the gameplay that this game is based on. Note: this does not have an effect your actual stats."
helpdocs_basic_on = "opts you into Duels. Running any command should opt you in, but this is the alternate way to do so. Your opt status will announce to the channel."
helpdocs_adv_1_on = "You can also use this command to have the bot primsg a nick to tell somebody join the fun."
helpdocs_basic_off = "opts you out of Duels. Your opt status will announce to the channel."
helpdocs_basic_admin = "allows bot admins to make changes to the game and player stats."
helpdocs_basic_devmode = "is used by bot admins to cause the game to bypass game-limiting features for a specific channel."
helpdocs_basic_game = "is used by bot admins to enable/disable the game for a specific channel."
helpdocs_basic_tier = "will display information about the channels progress in the game."
helpdocs_basic_author = "will display the author of Duels."
helpdocs_basic_version = "checks the last modified date of the Master branch of the game."
helpdocs_basic_deathblow = "checks to see if a recent combat provided you with the chance to finish a player."
helpdocs_basic_combat = "is the main function of gameplay. Target a player."
helpdocs_basic_usage = "is used to track your usage of the game. You can also specify a subcommand."
helpdocs_basic_streaks = "shows your current winning/losing streak. A streak is more than 2 in a row."
helpdocs_basic_bounty = "allows you to place a bounty on another player. This bounty can be won by the player that kills them. This should be incentive for players to gang up on another."
helpdocs_basic_harakiri = "is a suicide command. You will lose all your items and respawn. You must Confirm this command."
helpdocs_basic_weaponslocker = "allows you to add, remove, and view items in your weapons locker. These weapon names are included in combat, and provide a boost for having."
helpdocs_basic_leaderboard = "shows the top scores/stats of the game."
helpdocs_basic_warroom = "allows you to see what channel users are opted into the game and can be challenged."
helpdocs_basic_stats = "provides a brief sysnopsis of your current condition."
helpdocs_basic_loot = "shows the items you currently possess and can use. You may also buy, sell, and trade these items with the ingame store."
helpdocs_basic_health = "displays a detailed look at each bodyparts current status."
helpdocs_basic_magic = "allows you to use mana to do various magic functions."
helpdocs_basic_armor = "displays the current durability of any armor that you may possess."
helpdocs_basic_assault = "is a combat event that allows you to attack every other duels player."
helpdocs_basic_roulette = "allows you to risk a shot in the head for the chance at big coin winnings."
helpdocs_basic_monster = "allows you to do combat against a random low-level monster."
helpdocs_basic_random = "allows you to combat a random player. This has an added bonus if you win. There is a chance that the bot or monster may be selected. The bot always wins."
helpdocs_basic_colosseum = "pits all users against eachother with a prize that is based on the amount of players present."
helpdocs_basic_title = "allows you to set a vanity title in front of your nick during combat."
helpdocs_basic_mayhem = "is a combat event that finds every combination of duels possible."
helpdocs_basic_hungergames = "pits all duels players against eachother with one victorious."
helpdocs_basic_quest = "is a work in progress event that will pit multiple players against a high-level monster."
helpdocs_basic_grenade = "allows you to throw a grenade into the room. Damage is randomly based on who is able to jump out of the way."

## Monster List
monstersarray = [
"Aboleth","Beholder","Blue slaad","Chuul","Cloaker","Death kiss","Death slaad","Elder brain","Gauth","Gazer","Gibbering mouther","Gray slaad","Green slaad","Grell","Intellect devourer","Mind flayer","Mind flayer arcanist","Mindwitness","Morkoth","Neogi","Neogi master","Neothelid","Nothic",
"Otyugh","Red slaad","Spectator","Ulitharid","Allosaurus","Ankylosaurus","Ape","Aurochs","Axe beak","Baboon","Badger","Bat","Black bear","Blood hawk","Boar","Brontosaurus","Brown bear","Camel","Cat","Constrictor snake","Cow","Crab","Cranium rat","Crocodile","Deer","Deinonychus","Dimetrodon",
"Dire wolf","Draft horse","Eagle","Elephant","Elk","Giant ape","Giant bat","Giant boar","Giant centipede","Giant constrictor snake","Giant crab","Giant crocodile","Giant eagle","Giant elk","Giant frog","Giant goat","Giant hyena","Giant lizard","Giant octopus","Giant owl","Giant poisonous snake",
"Giant scorpion","Giant sea horse","Giant shark","Giant spider","Giant toad","Giant vulture","Giant wasp","Giant weasel","Giant wolf spider","Hadrosaurus","Hawk","Hunter shark","Hyena","Killer whale","Lion","Lizard","Mammoth","Octopus","Owl","Panther","Plesiosaurus","Polar bear","Pony",
"Quetzalcoatlus","Quipper","Rat","Reef shark","Rhinoceros","Saber-toothed tiger","Stegosaurus","Swarm of cranium rats","Swarm of insects","Swarm of poisonous snakes","Swarm of quippers","Swarm of rot grubs","Tiger","Triceratops","Tyrannosaurus rex","Couatl","Deva","Empyrean","Ki-rin","Pegasus",
"Planetar","Solar","Unicorn","Animated armor","Clay golem","Duodrone","Flesh golem","Flying sword","Helmed horror","Iron golem","Pentadrone","Quadrone","Rug of smothering","Scarecrow","Shield guardian","Stone golem","Tridrone","Adult black dragon","Adult blue dragon","Adult brass dragon",
"Adult bronze dragon","Adult copper dragon","Adult gold dragon","Adult green dragon","Adult red dragon","Adult silver dragon","Adult white dragon","Ancient black dragon","Ancient blue dragon","Ancient brass dragon","Ancient bronze dragon","Ancient copper dragon","Ancient gold dragon",
"Ancient green dragon","Ancient red dragon","Ancient silver dragon","Ancient white dragon","Black dragon wyrmling","Blue dragon wyrmling","Brass dragon wyrmling","Bronze dragon wyrmling","Copper dragon wyrmling","Dragon turtle","Faerie dragon","Gold dragon wyrmling","Green dragon wyrmling",
"Guard drake","Red dragon wyrmling","Silver dragon wyrmling","White dragon wyrmling","Wyvern","Young black dragon","Young blue dragon","Young brass dragon","Young bronze dragon","Young copper dragon","Young gold dragon","Young green dragon","Young red dragon","Young red shadow dragon",
"Young silver dragon","Young white dragon","Air elemental","Azer","Dao","Djinni","Dust mephit","Earth elemental","Efreeti","Fire elemental","Fire snake","Flail snail","Galeb duhr","Gargoyle","Ice mephit","Invisible stalker","Magma mephit","Magmin","Marid","Mud mephit","Salamander",
"Water elemental","Water weird","Xorn","Annis hag","Bheur hag","Blink dog","Darkling","Darkling elder","Dryad","Green hag","Korred","Meenlock","Pixie","Quickling","Redcap","Satyr","Sea hag","Yeth hound","Arcanaloth","Babau","Balor","Barbed devil","Barghest","Barlgura","Bearded devil",
"Bone devil","Cambion","Chain devil","Chasme","Devourer","Draegloth","Dretch","Erinyes","Glabrezu","Gnoll fang of Yeenoghu","Goristro","Hell hound","Hezrou","Horned devil","Ice devil","Imp","Incubus","Marilith","Maw demon","Mezzoloth","Nalfeshnee","Night hag","Nightmare","Nycaloth","Pit fiend",
"Quasit","Rakshasa","Shadow demon","Shoosuva","Spined devil","Succubus","Tanarukk","Ultroloth","Vargouille","Vrock","Yochlol","Cloud giant","Cloud giant smiling one","Cyclops","Ettin","Fire giant","Fire giant dreadnought","Fomorian","Frost giant","Frost giant everlasting one","Half-ogre",
"Hill giant","Mouth of Grolantor","Ogre","Oni","Stone giant","Stone giant dreamwalker","Storm giant","Storm giant quintessent","Troll","Aarakocra","Abjurer","Acolyte","Apprentice wizard","Archdruid","Archer","Archmage","Assassin","Bandit","Bandit captain","Bard","Berserker","Blackguard",
"Bugbear","Bugbear chief","Bullywug","Champion","Conjurer","Cult fanatic","Deep gnome","Deep scion","Diviner","Drow","Drow elite warrior","Drow mage","Drow priestess of Lolth","Druid","Duergar","Enchanter","Evoker","Firenewt","Firenewt warlock of Imix","Flind","Githyanki knight",
"Githyanki warrior","Githzerai monk","Githzerai zerth","Gladiator","Gnoll","Gnoll flesh gnawer","Gnoll hunter","Gnoll pack lord","Goblin","Goblin boss","Grimlock","Grung","Grung elite warrior","Grung wildling","Guard","Half-red dragon veteran","Hobgoblin","Hobgoblin captain",
"Hobgoblin devastator","Hobgoblin Iron Shadow","Hobgoblin warlord","Illusionist","Jackalwere","Kenku","Knight","Kobold dragonshield","Kobold inventor","Kobold scale sorcerer","Kraken priest","Kuo-toa","Kuo-toa archpriest","Kuo-toa monitor","Kuo-toa whip","Lizard king/queen","Lizardfolk",
"Lizardfolk shaman","Mage","Martial arts adept","Master thief","Necromancer","Nilbog","Orc","Orc Blade of Ilneval","Orc Claw of Luthic","Orc eye of Gruumsh","Orc Hand of Yurtrus","Orc Nurtured One of Yurtrus","Orc Red Fang of Shargaas","Orc war chief","Orog","Priest","Quaggoth",
"Quaggoth thonot","Sahuagin","Sahuagin baron","Sahuagin priestess","Sea spawn","Scout","Spy","Swashbuckler","Thri-kreen","Thug","Transmuter","Veteran","War priest","Warlock of the archfey","Warlock of the fiend","Warlock of the Great Old One","Warlord","Werebear","Wereboar","Wererat",
"Weretiger","Werewolf","Winged kobold","Xvart","Xvart warlock of Raxivort","Yuan-ti broodguard","Yuan-ti pureblood","Abominable yeti","Androsphinx","Ankheg","Banderhobb","Basilisk","Behir","Bulette","Carrion crawler","Catoblepas","Cave fisher","Centaur","Chimera","Chitine","Choldrith",
"Cockatrice","Darkmantle","Death dog","Displacer beast","Doppelganger","Drider","Ettercap","Froghemoth","Giant strider","Girallon","Gorgon","Grick","Grick alpha","Griffon","Guardian naga","Gynosphinx","Harpy","Hippogriff","Hook horror","Hydra","Kraken","Lamia","Leucrotta","Manticore",
"Medusa","Merrow","Mimic","Minotaur","Owlbear","Peryton","Phase spider","Piercer","Purple worm","Remorhaz","Roc","Roper","Rust monster","Shadow mastiff","Spirit naga","Tarrasque","Tlincalli","Trapper","Umber hulk","Winter wolf","Worg","Yeti","Young remorhaz","Yuan-ti abomination",
"Yuan-ti anathema","Yuan-ti malison","Yuan-ti mind whisperer","Yuan-ti nightmare speaker","Yuan-ti pit master","Black pudding","Gelatinous cube","Gray ooze","Ochre jelly","Slithering tracker","Awakened shrub","Awakened tree","Gas spore","Myconid adult","Myconid sovereign","Needle blight",
"Quaggoth spore servant","Shambling mound","Shrieker","Thorny","Treant","Twig blight","Vegepygmy chief","Wood woad","Alhoon","Adult blue dracolich","Banshee","Beholder zombie","Bodak","Bone naga","Crawling claw","Death knight","Death tyrant","Demilich","Flameskull","Ghast","Ghost","Ghoul",
"Gnoll witherling","Lich","Mind flayer lich","Minotaur skeleton","Mummy","Mummy lord","Ogre zombie","Poltergeist","Revenant","Shadow","Skeleton","Spawn of Kyuss","Specter","Vampire","Commoner","Frog","Giant fire beetle","Goat","Homunculus","Jackal","Lemure","Myconid sprout","Raven","Scorpion",
"Sea horse","Spider","Vulture","Weasel","Boggle","Cultist","Dolphin","Flumph","Flying snake","Giant rat","Kobold","Manes","Mastiff","Merfolk","Monodrone","Mule","Neogi hatchling","Noble","Poisonous snake""Slaad tadpole","Stirge","Tribal warrior","Pseudodragon","Pteranodon","Riding horse",
"Smoke mephit","Sprite","Steam mephit","Swarm of bats","Swarm of rats","Swarm of ravens","Troglodyte","Vegepygmy","Velociraptor","Violet fungus","Wolf","Zombie","Vine blight","Warhorse","Warhorse skeleton"]

########################
## Main Command Usage ##
########################

## work with /me ACTION (does not work with manual weapon)
@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
@module.intent('ACTION')
@module.require_chanmsg
def duel_action(bot, trigger):
    triggerargsarray = get_trigger_arg(bot, trigger.group(1), 'create')
    execute_main(bot, trigger, triggerargsarray, 'actionduel')

## bot.nick do this
@nickname_commands('duel')
def duel_nickcom(bot, trigger):
    channel_current = trigger.sender
    onscreentext(bot, channel_current, "Don't tell me what to do!")
    ## TODO maybe add the non-combat functions here?

## Base command
@sopel.module.commands('duel','challenge')
def mainfunction(bot, trigger):
    triggerargsarray = get_trigger_arg(bot, trigger.group(2), 'create')
    execute_main(bot, trigger, triggerargsarray, 'normalcom')

####################################
## Seperate Targets from Commands ##
####################################

#Class duels_channels(object):
#    #current = trigger.sender
#    dev = get_database_value(bot, duelrecorduser, 'devenabled') or []
#    def __init__(self, x):
#        self.x = x





def execute_main(bot, trigger, triggerargsarray, command_type):

    ## Instigator variable to describe the nickname that initiated the command
    instigator = trigger.nick

    ## Empty For now
    botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = [],[],[],[],[]

    ## First Command
    command_full = get_trigger_arg(bot, triggerargsarray, 0)
    command_main = get_trigger_arg(bot, triggerargsarray, 1)

    ## Channel the command was initiated in
    channel_current = trigger.sender


    bot.say(str(duels_character.setup.required))
    bot.say("stop")
    return
    
    ## Time when Module use started
    now = time.time()

    ## Check that the game is enabled in current channel. This is ignored if messaged in privmsg.
    duels_enabled_channels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
    if channel_current.startswith("#"):
        game_enabled_pass = check_game_enabled(bot, trigger, instigator, channel_current, duels_enabled_channels)
        if not game_enabled_pass:
            return

    ## This is a list of channels that can bypass checks
    duels_dev_channels = get_database_value(bot, duelrecorduser, 'devenabled') or []
    dev_bypass_checks = 0
    if channel_current in duels_dev_channels:
        dev_bypass_checks = 1

    ## Character Creation Check
    charactercreated = get_database_value(bot, duelrecorduser, 'charactercreatedb') or []
    if instigator not in charactercreated:
        if not [x for x in triggerargsarray if x == "-a"] and trigger.admin:
            if command_main != 'setup':
                dispmsgarray = []
                dispmsgarray.append("You need to run the character creation command    .duel setup   . Please include the following:")
                for j in duels_character_setup:
                    evallist = str('get_trigger_arg(bot, duels_character_setup_valid_'+j+', "list")')
                    evallist = eval(evallist)
                    dispmsgarray.append('-'+str(j).lower()+'="'+ evallist + '"')
                onscreentext(bot, ['say'], dispmsgarray)
            else:
                command_restructure = get_trigger_arg(bot, triggerargsarray, '2+')
                command_restructure = get_trigger_arg(bot, command_restructure, 'create')
                duels_command_function_setup(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, 'currenttier', channel_current, currentduelplayersarray, canduelarray, command_full , 'tiercommandeval', 'tierpepperrequired', 'tiermath', duels_dev_channels, 'commands_valid', duels_enabled_channels, 0, command_restructure)
            return

    ## Valid Commands
    commands_valid = duels_valid_commands(bot)

    ## Validate Instigator
    check_instigator_pass = check_instigator(bot, trigger, instigator, commands_valid, dev_bypass_checks, command_main)
    if not check_instigator_pass:
        return

    ## Check the command that was issued
    command_full_pass = check_command_full(bot, trigger, instigator, command_full, command_type)
    if not command_full_pass:
        return

    ## IF "&&" is in the full input, it is treated as multiple commands, and is split
    commands_array = []

    ## Build array of commands used
    if not [x for x in triggerargsarray if x == "&&"]:
        commands_array.append(command_full)
    else:
        command_full_split = command_full.split("&&")
        for command_split in command_full_split:
            commands_array.append(command_split)

    ## Cycle through command array
    for command_split_partial in commands_array:
        triggerargsarray_part = get_trigger_arg(bot, command_split_partial, 'create')
        duel_admin_switch = 0
        if [x for x in triggerargsarray_part if x == "-a"]:
            duel_admin_switch = 1
            triggerargsarray_part.remove("-a")

        ## Split commands to pass
        command_full_part = get_trigger_arg(bot, triggerargsarray_part, 0)
        command_main_part = get_trigger_arg(bot, triggerargsarray_part, 1)

        ## Block non-admin usage of the admin switch
        if duel_admin_switch and not trigger.admin:
            onscreentext(bot, ['say'], "The Admin Switch is meant for Bot Admin use only.")
            return

        ## Check if a deathblow is available to instigator
        deathblowcheck(bot, instigator) ## TODO

        ## Run command process
        command_main_process(bot, trigger, triggerargsarray_part, instigator, now, duels_dev_channels, commands_valid, command_full_part, command_main_part, channel_current, command_type, botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray, duels_enabled_channels, duel_admin_switch)

    ## bot does not need stats or backpack items
    refreshbot(bot)

    ## Instigator last used
    set_database_value(bot, instigator, 'lastcommand', now)

    ## Usage Counter
    adjust_database_value(bot, instigator, 'usage_total', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_total', 1)

    ## reset the game
    currenttier = get_database_value(bot, duelrecorduser, 'tier') or 0
    if currenttier >= 15:
        dispmsgarray = []
        dispmsgarray.append("Somebody has Triggered the Endgame! Stats will be reset.")
        duels_enabled_channels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
        onscreentext(bot, duels_enabled_channels, dispmsgarray)
        chanstatreset(bot)
        duelrecordwipe(bot)
        set_database_value(bot, duelrecorduser, 'chanstatsreset', now)

def command_main_process(bot, trigger, triggerargsarray, instigator, now, duels_dev_channels, commands_valid, command_full, command_main, channel_current, command_type, botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray, duels_enabled_channels, duel_admin_switch):

    ## Cheap error handling for people that like to find issues
    if command_main.isdigit():
        osd_notice(bot, instigator, "Commands can't be numbers.")
        return

    ## channel_current Block
    if command_main.lower() in duels_commands_inchannel  and not channel_current.startswith("#"):
        osd_notice(bot, instigator, "Duel " + command_main + " must be in channel.")
        return

    ## Instigator versus Bot
    if command_main.lower() == bot.nick.lower():
        onscreentext(bot, channel_current, "I refuse to fight a biological entity! If I did, you'd be sure to lose!")
        return

    ## Instigator versus Instigator
    if command_main.lower() == instigator.lower():
        onscreentext(bot, channel_current, "If you are feeling self-destructive, there are places you can call. Alternatively, you can run the harakiri command.")
        return

    ## Admin Command Blocker
    if command_main.lower() in duels_commands_admin and not duel_admin_switch:
        osd_notice(bot, instigator, "This admin function is only available to bot admins.")
        return

    ## Subcommand Versus Target
    if command_main.lower() in commands_valid:
        ## If command was issued as an action
        if command_type != 'actionduel':
            subcommands(bot, trigger, triggerargsarray, instigator, command_full , command_main, dueloptedinarray, botvisibleusers, now, currentuserlistarray, channel_current, currentduelplayersarray, canduelarray, duels_dev_channels,commands_valid, duels_enabled_channels, duel_admin_switch)
        else:
            osd_notice(bot, instigator, "Action duels should not be able to run commands. Targets Only")
        return

    ## Alternative Commands
    altcoms = alternative_commands_valid(bot)
    if command_main.lower() in altcoms:
        for subcom in duels_commands_alternate_list:
            duels_commands_alternate_eval = eval("duels_commands_alternate_"+subcom)
            if command_main.lower() in duels_commands_alternate_eval:
                command_main = subcom
                command_main_process(bot, trigger, triggerargsarray, instigator, now, duels_dev_channels, commands_valid, command_full, command_main, channel_current, command_type, botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray, duels_enabled_channels, duel_admin_switch)
        return

    ## Build User Lists if not there already
    if botvisibleusers == []:
        botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)

    ## Spell Check for non-nicks
    if command_main not in botvisibleusers:
        command_spelling_check(bot, trigger, triggerargsarray, instigator, now, duels_dev_channels, commands_valid, command_full, command_main, channel_current, command_type, botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray, altcoms, duels_enabled_channels, duel_admin_switch)
        return

    ##
    ## Anything Else is a Target For Dueling
    ##

    ## Rebuild user input
    command_full = get_trigger_arg(bot, command_full, 0)
    command_full = str("combat " + command_full)
    command_main = get_trigger_arg(bot, command_full, 1)
    triggerargsarray = get_trigger_arg(bot, command_full, 'create')

    ## Cycle back through with the subcommand "combat" as it will run various usage counters and such
    command_main_process(bot, trigger, triggerargsarray, instigator, now, duels_dev_channels, commands_valid, command_full, command_main, channel_current, command_type, botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray, duels_enabled_channels, duel_admin_switch)

########################
## Character Creation ##
########################

def duels_command_function_setup(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    charactercreated = get_database_value(bot, duelrecorduser, 'charactercreatedb') or []
    if instigator in charactercreated:
        if channel_current not in duels_dev_channels:
            onscreentext(bot, ['say'], "It looks like you have already created your character. This is done once at the beginning of your gameplay, and cannot be changed.")
            return

    ## Check valid switches
    mainsetupcheck = get_trigger_arg(bot, command_restructure, 0)
    if not mainsetupcheck:
        dispmsgarray = []
        dispmsgarray.append("You need to run a full character creation command    .duel setup   . Please include the following:")
        for j in duels_character_setup:
            evallist = str('get_trigger_arg(bot, duels_character_setup_valid_'+j+', "list")')
            evallist = eval(evallist)
            dispmsgarray.append('-'+str(j).lower()+'="'+ evallist + '"')
        onscreentext(bot, ['say'], dispmsgarray)
        return
        
    for x in duels_character_setup:
        switchcheck = find_switch_equal(bot, command_restructure, x.lower())
        validarray = eval("duels_character_setup_valid_" + x)
        validarraylist = get_trigger_arg(bot, validarray, "list")
        if not switchcheck:
            onscreentext(bot, ['say'], "Valid " + str(x)+ "s are: " + str(validarraylist) + '. Example setup command is        .duel setup -gender="male" -race="human" -class="paladin"')
            return
        if switchcheck not in validarray:
            onscreentext(bot, ['say'], str(switchcheck) + " is not a valid " + str(x)+ ". Options are: " + str(validarraylist) + ".")
            return
        set_database_value(bot, instigator, x, switchcheck)
    adjust_database_array(bot, duelrecorduser, [instigator], 'charactercreatedb', 'add')
    onscreentext(bot, ['say'], "Your character has been created. Enjoy the game!")
    
#######################
## Subcommands Usage ##
#######################

## Subcommands
def subcommands(bot, trigger, triggerargsarray, instigator, command_full , command_main, dueloptedinarray, botvisibleusers, now, currentuserlistarray, channel_current, currentduelplayersarray, canduelarray, duels_dev_channels,commands_valid, duels_enabled_channels, duel_admin_switch):

    ## Is the Tier Unlocked?
    currenttier = get_database_value(bot, duelrecorduser, 'tier') or 0
    tiercommandeval = tier_command(bot, command_main)
    tierpepperrequired = pepper_tier(bot, tiercommandeval)
    tiermath = int(tiercommandeval) - int(currenttier)
    if int(tiercommandeval) > int(currenttier):
        if command_main.lower() not in duels_commands_tier_self_use:
            if channel_current in duels_dev_channels or duel_admin_switch:
                allowpass = 1
            elif not channel_current.startswith("#") and len(duels_dev_channels) > 0:
                allowpass = 1
            else:
                onscreentext(bot, channel_current, "Duel " + command_main + " will be unlocked when somebody reaches " + str(tierpepperrequired) + ". " + str(tiermath) + " tier(s) remaining!")
                return

    ## Temporary during rewrite ## TODO
    if botvisibleusers == []:
        botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)

    ## Stamina Check
    staminapass = staminacheck(bot, instigator, channel_current, command_main.lower(), duel_admin_switch)
    if not staminapass:
        osd_notice(bot, instigator, "You do not have enough stamina to perform this action.")
        return

    ## Check to see that duels is not locked Out
    if command_main.lower() in duels_combat_lockout_list and channel_current not in duels_dev_channels and not duel_admin_switch:
        lockoutpass = check_duels_lockout(bot, instigator)
        if not lockoutpass:
            return
        set_database_value(bot, duelrecorduser, 'duelslockout', now)

    ## Stat check
    if command_main.lower() not in stat_check_commands_list:
        statreset(bot, instigator)
        healthcheck(bot, instigator)

    ## Canduelarray Check for certain commands
    if command_main.lower() in duels_commands_canduel_generate:
        ## Build User Lists if not there already
        if botvisibleusers == []:
            botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)
        if instigator not in canduelarray:
            canduel, validtargetmsg = duelcriteria(bot, instigator, command_main, currentduelplayersarray, channel_current, duel_admin_switch)
            osd_notice(bot, instigator, validtargetmsg)
            return

    ## Check bot is not a player for certain commands
    if command_main.lower() in duels_commands_canduel_remove_bot:
        ## Build User Lists if not there already
        if botvisibleusers == []:
            botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)
        if bot.nick in canduelarray:
            canduelarray.remove(bot.nick)

    ## Events Check
    if command_main.lower() in duels_commands_events:
        executedueling, executeduelingmsg = eventchecks(bot, canduelarray, command_main, instigator, currentduelplayersarray, channel_current, duel_admin_switch)
        if not executedueling:
            osd_notice(bot, instigator, executeduelingmsg)
            return

    ## If the above passes all above checks
    command_restructure = get_trigger_arg(bot, triggerargsarray, '2+')
    command_restructure = get_trigger_arg(bot, command_restructure, 'create')
    duels_command_function_run = str('duels_command_function_' + command_main.lower() + '(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure)')
    eval(duels_command_function_run)

    ## Don't allow multiple simultaneous dueling
    if command_main.lower() in duels_combat_lockout_list:
        reset_database_value(bot, duelrecorduser, 'duelslockout')

    ## Special Event
    if not channel_current.startswith("#") and command_main.lower() in duels_commands_special_events:
        speceventtext = ''
        speceventtotal = get_database_value(bot, duelrecorduser, 'specevent') or 0
        if speceventtotal >= 49:
            set_database_value(bot, duelrecorduser, 'specevent', 1)
            onscreentext(bot, [channel_current], instigator + " triggered the special event! Winnings are "+str(duel_special_event)+" Coins!")
            adjust_database_value(bot, instigator, 'coin', duel_special_event)
        else:
            adjust_database_value(bot, duelrecorduser, 'specevent', 1)

    ## Stamina charge
    staminacharge(bot, instigator, command_main.lower()) ## TODO make sure we only charge successful usage

    ## usage counter
    adjust_database_value(bot, instigator, 'usage_total', 1)
    adjust_database_value(bot, instigator, 'usage_'+command_main.lower(), 1)
    adjust_database_value(bot, duelrecorduser, 'usage_total', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_'+command_main.lower(), 1)

    ## reset the game
    currenttier = get_database_value(bot, duelrecorduser, 'tier') or 0
    if currenttier >= 15:
        dispmsgarray = []
        dispmsgarray.append("Somebody has Triggered the Endgame! Stats will be reset.")
        duels_enabled_channels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
        onscreentext(bot, duels_enabled_channels, dispmsgarray)
        chanstatreset(bot)
        duelrecordwipe(bot)
        set_database_value(bot, duelrecorduser, 'chanstatsreset', now)

#####################
## Main Duel Usage ##
#####################

def duel_combat(bot, instigator, maindueler, targetarray, triggerargsarray, now, channel_current, typeofduel, duels_dev_channels, duels_enabled_channels, duel_admin_switch):


    ## Same person can't instigate twice in a row
    set_database_value(bot, duelrecorduser, 'lastinstigator', maindueler)

    ## Starting Tier
    currenttierstart = get_database_value(bot, duelrecorduser, 'tier') or 0
    tierunlockweaponslocker = tier_command(bot, 'weaponslocker_complete')
    tierscaling = tierratio_level(bot)

    ## Monster
    if 'duelsmonster' in targetarray or maindueler == 'duelsmonster':
        duelsmonstername = get_trigger_arg(bot, monstersarray, 'random')
        set_database_value(bot, duelrecorduser, 'last_monster', duelsmonstername)
        if typeofduel != 'quest':
            duelmonsterlevel = str("A lower level "+duelsmonstername)
        else:
            duelmonsterlevel = str("A high level "+duelsmonstername)
        namemonster = duelsmonstername
        namemonstertext = str("The " + duelsmonstername)

    ## Manual Weapon Usage
    manualweapon = ''
    if currenttierstart >= tierunlockweaponslocker:
        manualweapon = find_switch_equal(bot, triggerargsarray, "w")

    ## Targetarray Start
    targetarraytotal = len(targetarray)
    for target in targetarray:

        ## target actual
        target = actualname(bot,target)

        ## Cleanup from Previous runs
        combattextarraycomplete = []
        texttargetarray = []
        deathblowarray = []

        ## Assault does not touch lastfought
        if typeofduel == 'assault' or typeofduel == 'quest':
            targetlastfoughtstart = get_database_value(bot, target, 'lastfought')

        ## Death Loop Start
        mainduelerdeathstart = get_database_value(bot, maindueler, 'assault_deaths') or 0

        ## Update Time Of Combat
        if duel_combat_timeouts == 'true':
            set_database_value(bot, maindueler, 'timeout_timeout', now)
            set_database_value(bot, target, 'timeout_timeout', now)
            set_database_value(bot, duelrecorduser, 'timeout_timeout', now)

        ## Display Naming
        if maindueler != 'duelsmonster':
            mainduelername = duel_names(bot, maindueler, channel_current)
        else:
            mainduelername = duelmonsterlevel
        mainduelerpepperstart = get_pepper(bot, maindueler)
        if target == maindueler:
            targetname = "themself"
        elif target == bot.nick:
            targetname = target
        elif target == 'duelsmonster':
            targetname = duelmonsterlevel
        else:
            targetname = duel_names(bot, target, channel_current)
        targetpepperstart = get_pepper(bot, target)

        ## Announce Combat
        announcetextarraycomplete = []
        announcetextarraycomplete.append(mainduelername + " versus " + targetname)
        if typeofduel == 'assault' or typeofduel == 'colosseum':
            onscreentext(bot, [maindueler,target], announcetextarraycomplete)
        elif typeofduel == 'quest':
            onscreentext(bot, [target], announcetextarraycomplete)
        else:
            onscreentext(bot, [channel_current], announcetextarraycomplete)
        
        ## Chance of maindueler finding loot
        if target != bot.nick and maindueler != target:
            randominventoryfind = randominventory(bot, maindueler)
            if randominventoryfind == 'true':
                loot = get_trigger_arg(bot, loot_winnable, 'random')
                loot_text = eval(loot+"dispmsg")
                combattextarraycomplete.append(maindueler + ' found a ' + str(loot) + ' ' + str(loot_text))

        ## Select winner Based on Stats
        if target == bot.nick:
            winner = bot.nick
            loser = maindueler
            losername = maindueler
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
                losername = maindueler
        if winner == maindueler:
            adjust_database_value(bot, maindueler, 'assault_wins', 1)
            adjust_database_value(bot, target, 'assault_losses', 1)
        else:
            if winner != 'duelsmonster' or winner != bot.nick:
                adjust_database_value(bot, maindueler, 'assault_losses', 1)
                adjust_database_value(bot, target, 'assault_wins', 1)

        ## Classes
        Classwinner = get_database_value(bot, winner, 'Class') or 'notClassy'
        Classloser = get_database_value(bot, loser, 'Class') or 'notClassy'

        ## races
        racewinner = get_database_value(bot, winner, 'race') or 'racist'
        raceloser = get_database_value(bot, loser, 'race') or 'racist'

        ## Current Streaks
        winner_loss_streak, loser_win_streak = get_current_streaks(bot, winner, loser)

        ## Update Wins and Losses
        if maindueler != target:
            adjust_database_value(bot, winner, 'wins', 1)
            adjust_database_value(bot, loser, 'losses', 1)
            set_current_streaks(bot, winner, 'win')
            set_current_streaks(bot, loser, 'loss')

        ## Manual weapon
        if winner == maindueler and manualweapon:
            if manualweapon == 'all':
                weapon = getallchanweaponsrandom(bot)
            elif manualweapon == 'target' or manualweapon == target:
                weapon = weaponofchoice(bot, target)
                weapon = str(target + "'s " + weapon)
            else:
                weapon = manualweapon
        elif winner == bot.nick or winner == 'duelsmonster':
            weapon = ''
        else:
            weapon = weaponofchoice(bot, winner)

        ## Format Weapon Name
        weapon = weaponformatter(bot, weapon)
        if weapon != '':
            weapon = str(" " + weapon)

        ## Magic Attributes Start
        winnershieldstart, winnercursestart = get_current_magic_attributes(bot, winner)
        losershieldstart, losercursestart = get_current_magic_attributes(bot, loser)

        ## Body Part Hit
        bodypart, bodypartname = bodypart_select(bot, loser)

        ## Strike Type
        striketype = get_trigger_arg(bot, duel_hit_types, 'random')

        ## Damage
        if Classloser == 'rogue' and loser != 'duelsmonster' and winner != 'duelsmonster':
            if winner == loser or winner == bot.nick:
                damage = 0
                damagetext = str(loser + " takes no damage in this encounter")
            else:
                damage = duels_damage(bot, tierscaling, Classwinner, racewinner, Classloser, winner, loser)
                damage = int(damage)
                damagetext = duels_damage_text(bot, damage, winner, loser, bodypart, striketype, weapon, Classwinner, racewinner, bodypartname)
        elif loser == 'duelsmonster':
            damage = 0
            damagetext = str(winner + " slays the " + namemonster +  weapon + ".")
        elif winner == 'duelsmonster':
            damage = duels_damage(bot, tierscaling, Classwinner, racewinner, Classloser, winner, loser)
            damage = int(damage)
            damagetext = duels_damage_text(bot, damage, namemonstertext, loser, bodypart, striketype, weapon, Classwinner, racewinner, bodypartname)
        else:
            damage = duels_damage(bot, tierscaling, Classwinner, racewinner, Classloser, winner, loser)
            damage = int(damage)
            damagetext = duels_damage_text(bot, damage, winner, loser, bodypart, striketype, weapon, Classwinner, racewinner, bodypartname)
        combattextarraycomplete.append(damagetext)

        ## Vampires gain health from wins
        if racewinner == 'vampire' and winner != loser:
            splitdamage = int(damage) / len(stats_healthbodyparts)
            for part in stats_healthbodyparts:
                adjust_database_value(bot, winner, part, splitdamage)

        ## Berserker Rage
        if racewinner == 'barbarian' and winner != loser and loser != 'duelsmonster':
            rageodds = randint(1, duel_advantage_barbarian_rage_chance)
            if rageodds == 1:
                extradamage = randint(1, duel_advantage_barbarian_rage_max)
                combattextarraycomplete.append(winner + " goes into Berserker Rage for an extra " + str(extradamage) + " damage.")
                extradamage = extradamage * tierscaling
                damage = damage + extradamage

        ## Paladin deflect
        persontotakedamage = loser
        if Classloser == 'paladin' and damage > 0 and winner != loser and loser != 'duelsmonster':
            deflectodds = randint(1, duel_advantage_paladin_deflect_chance)
            if deflectodds == 1:
                persontotakedamage = winner
                combattextarraycomplete.append(loser + " deflects the damage back on " + winner + ". ")
                damage, damagetextarray = damage_resistance(bot, winner, damage, bodypart)
                for x in damagetextarray:
                    combattextarraycomplete.append(x)
                if damage > 0:
                    if winner == maindueler:
                        adjust_database_value(bot, target, 'assault_damagetaken', damage)
                        adjust_database_value(bot, target, 'assault_damagedealt', damage)
                    else:
                        adjust_database_value(bot, maindueler, 'assault_damagedealt', damage)
                        adjust_database_value(bot, target, 'assault_damagetaken', damage)
                    adjust_database_value(bot, loser, bodypart, -abs(damage))
                    ## Update Health Of winner, respawn, allow loser to loot
                    winnerheadhealth = get_database_value(bot, winner, 'head')
                    winnertorsohealth = get_database_value(bot, winner, 'torso')
                    totalhealthwinner = get_health(bot,winner)
                    if winnerheadhealth  <= 0 or winnertorsohealth <= 0:
                        if winner == maindueler:
                            adjust_database_value(bot, maindueler, 'assault_deaths', 1)
                            adjust_database_value(bot, target, 'assault_kills', 1)
                        else:
                            adjust_database_value(bot, maindueler, 'assault_kills', 1)
                            adjust_database_value(bot, target, 'assault_deaths', 1)
                        loserkilledwinner = whokilledwhom(bot, loser, winner) or ''
                        for x in loserkilledwinner:
                            combattextarraycomplete.append(x)
                    elif totalhealthwinner < 100 and typeofduel == 'target':
                        set_database_value(bot, loser, 'deathblowtarget', winner)
                        set_database_value(bot, loser, 'deathblowtargettime', now)
                        deathblowarray.append(loser + " has a chance of striking a deathblow on " + winner)
                    else:
                        winnercurrenthealthbody  = get_database_value(bot, winner, bodypart)
                        if winnercurrenthealthbody  <= 0:
                            combattextarraycomplete.append(winner + "'s " + bodypartname + " has become crippled!")
                damage = 0

        ## Damage Resist
        if damage > 0 and loser != 'duelsmonster':
            damage, damagetextarray = damage_resistance(bot, loser, damage, bodypart)
            for x in damagetextarray:
                combattextarraycomplete.append(x)
            if damage > 0:
                if winner == maindueler:
                    adjust_database_value(bot, maindueler, 'assault_damagedealt', damage)
                    adjust_database_value(bot, target, 'assault_damagetaken', damage)
                else:
                    adjust_database_value(bot, maindueler, 'assault_damagetaken', damage)
                    adjust_database_value(bot, target, 'assault_damagedealt', damage)
                adjust_database_value(bot, loser, bodypart, -abs(damage))
                ## Update Health Of loser, respawn, allow winner to loot
                loserheadhealth = get_database_value(bot, loser, 'head')
                losertorsohealth = get_database_value(bot, loser, 'torso')
                totalhealthloser = get_health(bot,loser)
                if loserheadhealth  <= 0 or losertorsohealth <= 0:
                    if winner == maindueler:
                        adjust_database_value(bot, maindueler, 'assault_kills', 1)
                        adjust_database_value(bot, target, 'assault_deaths', 1)
                    else:
                        adjust_database_value(bot, maindueler, 'assault_deaths', 1)
                        adjust_database_value(bot, target, 'assault_kills', 1)
                    winnerkilledloser = whokilledwhom(bot, winner, loser) or ''
                    for x in winnerkilledloser:
                        combattextarraycomplete.append(x)
                elif totalhealthloser < 100 and typeofduel == 'target':
                    set_database_value(bot, winner, 'deathblowtarget', loser)
                    set_database_value(bot, winner, 'deathblowtargettime', now)
                    deathblowarray.append(winner + " has a chance of striking a deathblow on " + loser)
                else:
                    losercurrenthealthbody  = get_database_value(bot, loser, bodypart)
                    if losercurrenthealthbody  <= 0:
                        combattextarraycomplete.append(loser + "'s " + bodypartname + " has become crippled!")

        ## Knight Retaliation
        if Classloser == 'knight' and winner != loser and loser != 'duelsmonster':
            retaliateodds = randint(1, duel_advantage_knight_retaliate_chance)
            if retaliateodds == 1:
                ## Weapon
                weaponb = weaponofchoice(bot, loser)
                weaponb = weaponformatter(bot, weaponb)
                weaponb = str(" "+ weaponb)
                ## Body Part Hit
                bodypartb, bodypartnameb = bodypart_select(bot, winner)
                ## Strike Type
                striketypeb = get_trigger_arg(bot, duel_hit_types, 'random')
                ## Damage
                damageb = duels_damage(bot, tierscaling, Classloser, raceloser, Classwinner, loser, winner)
                damagetextb = duels_damage_text(bot, damage, loser, winner, bodypartb, striketypeb, weaponb, Classloser, raceloser, bodypartnameb)
                combattextarraycomplete.append(damagetextb)
                ## Damage Resist
                if damage > 0:
                    damage, damagetextarray = damage_resistance(bot, loser, damage, bodypart)
                    for x in damagetextarray:
                        combattextarraycomplete.append(x)
                    if damage > 0:
                        if winner == maindueler:
                            adjust_database_value(bot, maindueler, 'assault_damagetaken', damage)
                            adjust_database_value(bot, target, 'assault_damagedealt', damage)
                        else:
                            adjust_database_value(bot, maindueler, 'assault_damagedealt', damage)
                            adjust_database_value(bot, target, 'assault_damagetaken', damage)
                        adjust_database_value(bot, winner, bodypartb, -abs(damage))
                        ## Update Health Of winner, respawn, allow loser to loot
                        winnerheadhealth = get_database_value(bot, winner, 'head')
                        winnertorsohealth = get_database_value(bot, winner, 'torso')
                        totalhealthwinner = get_health(bot,winner)
                        if winnerheadhealth  <= 0 or winnertorsohealth <= 0:
                            if winner == maindueler:
                                adjust_database_value(bot, maindueler, 'assault_deaths', 1)
                                adjust_database_value(bot, target, 'assault_kills', 1)
                            else:
                                adjust_database_value(bot, maindueler, 'assault_kills', 1)
                                adjust_database_value(bot, target, 'assault_deaths', 1)
                            loserkilledwinner = whokilledwhom(bot, loser, winner) or ''
                            for x in loserkilledwinner:
                                combattextarraycomplete.append(x)
                        elif totalhealthwinner < 100 and typeofduel == 'target':
                            set_database_value(bot, loser, 'deathblowtarget', winner)
                            set_database_value(bot, loser, 'deathblowtargettime', now)
                            deathblowarray.append(loser + " has a chance of striking a deathblow on " + winner)
                        else:
                            winnercurrenthealthbody  = get_database_value(bot, winner, bodypart)
                            if winnercurrenthealthbody  <= 0:
                                combattextarraycomplete.append(winner + "'s " + bodypartnameb + " has become crippled!")

        ## Chance that maindueler loses found loot
        mainduelerdeathend = get_database_value(bot, maindueler, 'assault_deaths') or 0
        if target != bot.nick and maindueler != target and mainduelerdeathend == mainduelerdeathstart:
            if randominventoryfind == 'true':
                ## Barbarians get a 50/50 chance of getting loot even if they lose
                Classloser = get_database_value(bot, loser, 'Class') or 'notClassy'
                raceloser = get_database_value(bot, loser, 'race') or 'racist'
                barbarianstealroll = randint(0, 100)
                if raceloser == 'barbarian' and barbarianstealroll >= 50 and loser != 'duelsmonster':
                    combattextarraycomplete.append(loser + " steals the " + str(loot))
                    lootwinner = loser
                elif winner == target and loser != 'duelsmonster':
                    combattextarraycomplete.append(winner + " gains the " + str(loot))
                    lootwinner = winner
                else:
                    lootwinner = winner
                if lootwinner != 'duelsmonster':
                    adjust_database_value(bot, lootwinner, loot, 1)
                    if lootwinner == maindueler:
                        adjust_database_value(bot, maindueler, 'assault_potionswon', 1)
                        adjust_database_value(bot, target, 'assault_potionslost', 1)
                    else:
                        adjust_database_value(bot, maindueler, 'assault_potionslost', 1)
                        adjust_database_value(bot, target, 'assault_potionswon', 1)

        ## Update XP points
        if Classwinner == 'ranger':
            XPearnedwinner = xp_winner_ranger
        else:
            XPearnedwinner = xp_winner
        if Classloser == 'ranger':
            XPearnedloser = xp_loser_ranger
        else:
            XPearnedloser = xp_loser
        if maindueler != target and target != bot.nick:
            if winner != 'duelsmonster' and loser != 'duelsmonster':
                winnertier = get_database_value(bot, winner, 'tier')
                losertier = get_database_value(bot, loser, 'tier')
                if winnertier < currenttierstart:
                    XPearnedwinner = XPearnedwinner * tierscaling
                if losertier < currenttierstart:
                    XPearnedloser = XPearnedloser * tierscaling
                adjust_database_value(bot, winner, 'xp', XPearnedwinner)
                adjust_database_value(bot, loser, 'xp', XPearnedloser)
                if winner == maindueler:
                    adjust_database_value(bot, maindueler, 'assault_xp', XPearnedwinner)
                    adjust_database_value(bot, target, 'assault_xp', XPearnedloser)
                else:
                    adjust_database_value(bot, maindueler, 'assault_xp', XPearnedloser)
                    adjust_database_value(bot, target, 'assault_xp', XPearnedwinner)

        ## Streaks Text
        if maindueler != target:
            if winner == 'duelsmonster':
                streaktext = get_streaktext(bot, namemonstertext, loser, winner_loss_streak, loser_win_streak) or ''
            elif loser == 'duelsmonster':
                streaktext = get_streaktext(bot, winner, namemonstertext, winner_loss_streak, loser_win_streak) or ''
            else:
                streaktext = get_streaktext(bot, winner, loser, winner_loss_streak, loser_win_streak) or ''
            if streaktext != '':
                combattextarraycomplete.append(streaktext)

        ## new pepper level?
        mainduelerpeppernow = get_pepper(bot, maindueler)
        if mainduelerpeppernow != mainduelerpepperstart and maindueler != target and maindueler != 'duelsmonster':
            combattextarraycomplete.append(maindueler + " graduates to " + mainduelerpeppernow + "! ")
            adjust_database_value(bot, maindueler, 'assault_levelups', 1)
        targetpeppernow = get_pepper(bot, target)
        if targetpeppernow != targetpepperstart and maindueler != target and target != bot.nick and target != 'duelsmonster':
            adjust_database_value(bot, target, 'assault_levelups', 1)
            combattextarraycomplete.append(target + " graduates to " + targetpeppernow + "! ")

        ## Tier update
        currenttierend = get_database_value(bot, duelrecorduser, 'tier') or 1
        if int(currenttierend) > int(currenttierstart):
            combattextarraycomplete.append("New Tier Unlocked!")
            tiercheck = eval("duels_commands_tier_unlocks_"+str(currenttierend))
            if tiercheck != []:
                newtierlist = get_trigger_arg(bot, tiercheck, "list")
                combattextarraycomplete.append("Feature(s) now available: " + newtierlist)

        ## Magic Attributes text
        if maindueler != target:
            magicattributestext = get_magic_attributes_text(bot, winner, loser, winnershieldstart, losershieldstart, winnercursestart , losercursestart)
            for x in magicattributestext:
                combattextarraycomplete.append(x)

        ## Random Bonus
        if typeofduel == 'random' and winner == maindueler and winner != bot.nick and winner != loser and winner != 'duelsmonster':
            adjust_database_value(bot, winner, 'coin', random_payout)
            combattextarraycomplete.append(maindueler + " won the random attack payout of " + str(random_payout)+ " coin!")

        ## On Screen Text
        if typeofduel == 'assault' or typeofduel == 'colosseum':
            onscreentext(bot, [winner,loser], combattextarraycomplete)
        elif typeofduel == 'quest':
            onscreentext(bot, [target], combattextarraycomplete)
        else:
            onscreentext(bot, [channel_current], combattextarraycomplete)


        ## deathblow text
        if typeofduel == 'target' and deathblowarray != [] and 'duelsmonster' not in deathblowarray:
            onscreentext(bot, [channel_current], deathblowarray)

        ## Pause Between duels
        if typeofduel == 'assault':
            bot.notice("  ", maindueler)
            #time.sleep(randint(2, 5)) # added to protect bot from "excess flood"

        ## Update last fought
        if maindueler != target and typeofduel != 'assault' and typeofduel != 'colosseum' and typeofduel != 'quest':
            if maindueler == 'duelsmonster':
                set_database_value(bot, target, 'lastfought', mainduelername)
            else:
                set_database_value(bot, target, 'lastfought', maindueler)
            if target == 'duelsmonster':
                set_database_value(bot, maindueler, 'lastfought', targetname)
            else:
                set_database_value(bot, maindueler, 'lastfought', target)

        ## End Of assault
        if typeofduel == 'assault' or typeofduel == 'quest':
            set_database_value(bot, target, 'lastfought', targetlastfoughtstart)

#################
## Subcommands ##
#################

## Combat Subcommand
def duels_command_function_combat(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    ## Build User Lists if not there already
    if botvisibleusers == []:
        botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)

    ## Who is the target
    target = get_trigger_arg(bot, [x for x in command_restructure if x in botvisibleusers], 1) or instigator
    validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
    if not validtarget:
        osd_notice(bot, instigator, validtargetmsg)
        return
    target = actualname(bot, target)

    ## Check that the target doesn't have a timeout preventing them from playing
    executedueling, executeduelingmsg = duelcriteria(bot, instigator, target, currentduelplayersarray, channel_current, duel_admin_switch)
    if not executedueling:
        osd_notice(bot, instigator, executeduelingmsg)
        return

    ## Run the duel
    duel_combat(bot, instigator, instigator, [target], command_restructure, now, channel_current, 'target', duels_dev_channels, duels_enabled_channels, duel_admin_switch)

## Author Subcommand
def duels_command_function_author(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    onscreentext(bot, channel_current, "The author of Duels is deathbybandaid. Credit to DGW for the original game. Run .duel Classic to see his version.")

## Classic Duels by DGW
def duels_command_function_Classic(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    inputtarget = get_trigger_arg(bot, triggerargsarray, 2) or ''
    if inputtarget == 'stats':
        inputtarget = get_trigger_arg(bot, triggerargsarray, 3) or instigator
        return duelClassic_stats(bot, trigger, inputtarget)
    elif inputtarget == 'leaderboard':
        winrateplayers,winratescores = [],[]
        bestwinsplayers,bestwinscores = [],[]
        worstlossesplayers,worstlossesscores = [],[]
        for player in canduelarray:
            wins, losses = get_duels(bot, player)
            total = wins + losses
            if total:
                win_rate = wins / total * 100
                winrateplayers.append(player)
                winratescores.append(win_rate)
            best_wins = get_best_win_streak(bot, player)
            if best_wins:
                bestwinsplayers.append(player)
                bestwinscores.append(best_wins)
            worst_losses = get_worst_loss_streak(bot, player)
            if worst_losses:
                worstlossesplayers.append(player)
                worstlossesscores.append(worst_losses)
        winratescores, winrateplayers = array_arrangesort(bot, winratescores, winrateplayers)
        bestwinscores, bestwinsplayers = array_arrangesort(bot, bestwinscores, bestwinsplayers)
        worstlossesscores, worstlossesplayers = array_arrangesort(bot, worstlossesscores, worstlossesplayers)
        Classicleaderboardmessage = []
        if winrateplayers != []:
            winrateleadername = get_trigger_arg(bot, winrateplayers, 'last')
            winrateleadernumber = get_trigger_arg(bot, winratescores, 'last')
            winrateleadernumber = format(winrateleadernumber, '.3f')
            Classicleaderboardmessage.append("Best win rate is " + winrateleadername + " with " + str(winrateleadernumber))
        if bestwinsplayers != []:
            bestwinleadername = get_trigger_arg(bot, bestwinsplayers, 'last')
            bestwinleadernumber = get_trigger_arg(bot, bestwinscores, 'last')
            Classicleaderboardmessage.append("Worst losing streak is " + bestwinleadername + " with " + str(bestwinleadernumber))
        if worstlossesplayers != []:
            worstlossessleadername = get_trigger_arg(bot, worstlossesplayers, 'last')
            worstlossesleadernumber = get_trigger_arg(bot, worstlossesscores, 'last')
            Classicleaderboardmessage.append("Best win streak is " + worstlossessleadername + " with " + str(worstlossesleadernumber))
        onscreentext(bot, ['say'], Classicleaderboardmessage)
    else:
        ## Build User Lists if not there already
        if botvisibleusers == []:
            botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)
        validtarget, validtargetmsg = targetcheck(bot, inputtarget, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
        if not validtarget:
            onscreentext(bot, [instigator], validtargetmsg)
            return
        duels_Classic_timeout = 600
        if channel_current in duels_dev_channels or duel_admin_switch:
            duels_Classic_timeout = 0
        return duelClassic(bot, channel_current, instigator, inputtarget, duels_Classic_timeout, is_admin=trigger.admin)

## Version
def duels_command_function_version(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    versionfetch = versionnumber(bot)
    onscreentext(bot, channel_current, "The duels framework was last modified on " + str(versionfetch) + ".")

## Docs Subcommand
def duels_command_function_docs(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    ## Build User Lists if not there already
    if botvisibleusers == []:
        botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)

    altcoms = alternative_commands_valid(bot)
    endmessage = []

    target = get_trigger_arg(bot, [x for x in command_restructure if x in botvisibleusers], 1) or channel_current
    if target != instigator and target != channel_current:
        validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return

    messagetype = get_trigger_arg(bot, [x for x in command_restructure if x in altcoms or x in commands_valid or x == "-a"], 1) or 'main'
    if messagetype in altcoms or messagetype in commands_valid:
        if messagetype in duels_commands_alternate_docs or messagetype == 'docs':
            messagetype = "docs"
        else:
            for subcom in duels_commands_alternate_list:
                duels_commands_alternate_eval = eval("duels_commands_alternate_"+subcom)
                if messagetype.lower() in duels_commands_alternate_eval:
                    messagetype = subcom

    if messagetype != 'main':
        if messagetype in duels_commands_alternate_docs or messagetype == 'docs':
            endmessage.append("Online Docs: " + GITWIKIURL)
        else:

            ## Admin Only
            if messagetype.lower() in duels_commands_admin:
                endmessage.append("[ADMIN ONLY]")

            ## Command Name
            endmessage.append("Basic info for Duel " + messagetype + ":")

            ## Basic info
            try:
                help_run = str('helpdocs_basic_' + messagetype.lower())
                endmessageeval = eval(help_run)
                endmessage.append(endmessageeval)
            except NameError:
                dummyvar = ""

            ## Advanced info
            for i in range(0,16):
                try:
                    help_run = str('helpdocs_adv_'+str(i)+"_" + messagetype.lower())
                    endmessageeval = eval(help_run)
                    endmessage.append(endmessageeval)
                except NameError:
                    continue

            ## Alternate Commands
            if messagetype in duels_commands_alternate_list:
                duels_commands_alternate_evalb = eval("duels_commands_alternate_"+messagetype)
                alternatelist = get_trigger_arg(bot, duels_commands_alternate_evalb, 'list')
                endmessage.append("Alternate Command(s) = "+alternatelist)

            ## Tier
            commandtier = tier_command(bot, messagetype)
            commandpepper = pepper_tier(bot, commandtier)
            if messagetype.lower() in duels_commands_tier_self_use:
                endmessage.append("Self-usable from the beginning of the game, but not use on others. It is unlocked at tier " + str(commandtier)+ " ("+ str(commandpepper.title()) + ").")
            else:
                endmessage.append("Unlocked at tier " + str(commandtier)+ " ("+ str(commandpepper.title()) + ").")

            ## Stamina Costs
            commandstaminacost = 0
            if messagetype not in duels_commands_stamina_free:
                commandstaminacost = eval("duels_commands_stamina_"+messagetype)
            endmessage.append("Costs " + str(commandstaminacost) + " stamina.")

            if messagetype.lower() in duels_commands_inchannel:
                endmessage.append("Must be run in channel.")

            if messagetype.lower() in duels_commands_special_events:
                endmessage.append("Eligible for the 50th usage payout of " + str(duel_special_event) + " coins!")

            ## timeout
            try:
                help_run = str('timeout_' + messagetype.lower())
                endmessageeval = eval(help_run)
                endmessage.append("Has a timeout of " + str(hours_minutes_seconds(endmessageeval))+ "between uses.")
            except NameError:
                dummyvar = ""

    ## Defaults
    else:
        endmessage.append("Online Docs: " + GITWIKIURL)
    onscreentext(bot, [target], endmessage)

## On Subcommand
def duels_command_function_on(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    ## Build User Lists if not there already
    if botvisibleusers == []:
        botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)

    target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
    if target and target != instigator:
        if target == 'all' or target == 'everyone':
            duels_enabled_channels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
            if not duel_admin_switch:
                onscreentext(bot, duels_enabled_channels, instigator + " thinks everybody should play duels!")
            else:
                onscreentext(bot, duels_enabled_channels, instigator + " enabled duels for everyone!")
                adjust_database_array(bot, duelrecorduser, botvisibleusers, 'duelusers', 'add')
            return
        validtarget, validtargetmsg = nickcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
        if target.lower() in [x.lower() for x in dueloptedinarray]:
            osd_notice(bot, instigator, "It looks like " + target + " already has duels on.")
            return
        reasonmessage = get_trigger_arg(bot, triggerargsarray, '3+')
        if not reasonmessage:
            if not duel_admin_switch:
                osd_notice(bot, instigator, "if you would like " + target + " to play duels, you can run this command along with a message, that they will get privately.")
            else:
                osd_notice(bot, instigator, "you must include a message to send to " + target + " as to why you are changing their opt-in status to on.")
            return
        else:
            if duel_admin_switch:
                osd_notice(bot, target, instigator + " enabled duels for you for the following reason: " + str(reasonmessage)+ ".")
            else:
                osd_notice(bot, target, instigator + " thinks you should opt into duels for the following reason: " + str(reasonmessage)+ ". To opt in, run .duel on.")
                return

    ## User can't toggle status all the time
    targetopttime = get_timesince_duels(bot, target, 'timeout_opttime')
    if targetopttime < timeout_opt:
        if channel_current in duels_dev_channels or duel_admin_switch:
            allowpass = 1
        elif not channel_current.startswith("#") and len(duels_dev_channels) > 0:
            allowpass = 1
        elif duel_admin_switch and target != instigator:
            allowpass = 1
        else:
            osd_notice(bot, instigator, "It looks like you can't enable/disable duels for " + str(hours_minutes_seconds((timeout_opt - targetopttime))) + ".")
            return

    ## check if player already has duels on
    if target.lower() in [x.lower() for x in dueloptedinarray] and target == instigator:
        osd_notice(bot, instigator, "It looks like you already have duels on.")
        return

    ## make the adjustment
    adjust_database_array(bot, duelrecorduser, [target], 'duelusers', 'add')
    set_database_value(bot, target, 'timeout_opttime', now)
    if target == instigator:
        osd_notice(bot, instigator, "Duels should now be " +  command_main + " for you.")
    elif target != instigator and duel_admin_switch:
        osd_notice(bot, instigator, "Duels should now be " +  command_main + " for " + target + ".")

    ## Anounce to channels
    duels_enabled_channels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
    dispmsgarray = []
    if target != instigator:
        dispmsgarray.append(target + " has entered the arena!")
    else:
        dispmsgarray.append(target + " has entered the arena!")
    onscreentext(bot, duels_enabled_channels, dispmsgarray)

## Off Subcommand
def duels_command_function_off(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    ## Build User Lists if not there already
    if botvisibleusers == []:
        botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)

    target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
    if target and target != instigator:
        if target == 'all' or target == 'everyone':
            duels_enabled_channels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
            if not duel_admin_switch:
                onscreentext(bot, duels_enabled_channels, instigator + " thinks everybody should stop playing duels!")
            else:
                onscreentext(bot, duels_enabled_channels, instigator + " disabled duels for everyone!")
                reset_database_value(bot, duelrecorduser, 'duelusers')
            return
        validtarget, validtargetmsg = nickcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
        if target.lower() not in [x.lower() for x in dueloptedinarray]:
            osd_notice(bot, instigator, "It looks like " + target + " already has duels off.")
            return
        reasonmessage = get_trigger_arg(bot, triggerargsarray, '3+')
        if not reasonmessage:
            if not duel_admin_switch:
                osd_notice(bot, instigator, "if you would like " + target + " to disable duels, you can run this command along with a message, that they will get privately.")
            else:
                osd_notice(bot, instigator, "you must include a message to send to " + target + " as to why you are changing their opt-in status to off.")
            return
        else:
            if duel_admin_switch:
                osd_notice(bot, target, instigator + " disabled duels for you for the following reason: " + str(reasonmessage)+ ".")
            else:
                osd_notice(bot, target, instigator + " thinks you should opt out of duels for the following reason: " + str(reasonmessage)+ ". To opt out, run .duel off.")
                return

    ## User can't toggle status all the time
    targetopttime = get_timesince_duels(bot, target, 'timeout_opttime')
    if targetopttime < timeout_opt:
        if channel_current in duels_dev_channels or duel_admin_switch:
            allowpass = 1
        elif not channel_current.startswith("#") and len(duels_dev_channels) > 0:
            allowpass = 1
        elif duel_admin_switch and target != instigator:
            allowpass = 1
        else:
            osd_notice(bot, instigator, "It looks like you can't enable/disable duels for " + str(hours_minutes_seconds((timeout_opt - targetopttime))) + ".")
            return

    ## check if player already has duels on
    if target.lower() not in [x.lower() for x in dueloptedinarray] and target == instigator:
        osd_notice(bot, instigator, "It looks like you already have duels off.")
        return

    ## make the adjustment
    adjust_database_array(bot, duelrecorduser, [target], 'duelusers', 'del')
    set_database_value(bot, target, 'timeout_opttime', now)
    if target == instigator:
        osd_notice(bot, instigator, "Duels should now be " +  command_main + " for you.")
    elif target != instigator and duel_admin_switch:
        osd_notice(bot, instigator, "Duels should now be " +  command_main + " for " + target + ".")

    ## Anounce to channels
    duels_enabled_channels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
    dispmsgarray = []
    if target == instigator:
        cowardterm = get_trigger_arg(bot, cowardarray, 'random')
        dispmsgarray.append(target + " has left the arena! " + cowardterm)
    else:
        dispmsgarray.append(target + " has left the arena! ")
    onscreentext(bot, duels_enabled_channels, dispmsgarray)

## Enable game
def duels_command_function_game(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    channeltarget = get_trigger_arg(bot, [x for x in triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        osd_notice(bot, instigator, "You must specify a valid channel.")
        return

    command = get_trigger_arg(bot, [x for x in triggerargsarray if x == 'on' or x == 'off'], 1)
    if not command:
        osd_notice(bot, instigator, "you must specify if you want the channel on or off.")
        return

    valid_channel_list = valid_bot_channels(bot)
    if channeltarget not in valid_channel_list:
        osd_notice(bot, instigator, "I don't appear to be in that channel.")
        return

    if command == 'on':
        if channeltarget in duels_enabled_channels:
            osd_notice(bot, instigator, "Duels is already on in " + channel_current + ".")
            return
        adjust_database_array(bot, duelrecorduser, [channeltarget], 'gameenabled', 'add')
        onscreentext(bot, channeltarget, "Duels has been enabled in " + channeltarget + "!")
    elif command == 'off':
        if channeltarget not in duels_enabled_channels:
            osd_notice(bot, instigator, "Duels is already off in " + channeltarget + ".")
            return
        adjust_database_array(bot, duelrecorduser, [channeltarget], 'gameenabled', 'del')
        onscreentext(bot, channeltarget, "Duels has been disabled in " + channeltarget + "!")
    else:
        osd_notice(bot, instigator, "Invalid command.")

## dev bypass
def duels_command_function_devmode(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    channeltarget = get_trigger_arg(bot, [x for x in triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        osd_notice(bot, instigator, "You must specify a valid channel.")
        return

    command = get_trigger_arg(bot, [x for x in triggerargsarray if x == 'on' or x == 'off'], 1)
    if not command:
        osd_notice(bot, instigator, "you must specify if you want the channel on or off.")
        return

    valid_channel_list = valid_bot_channels(bot)
    if channeltarget not in valid_channel_list:
        osd_notice(bot, instigator, "I don't appear to be in that channel.")
        return

    if command == 'on':
        if channeltarget in duels_dev_channels:
            osd_notice(bot, instigator, "Duels devmode is already on in " + channel_current + ".")
            return
        adjust_database_array(bot, duelrecorduser, [channeltarget], 'devenabled', 'add')
        onscreentext(bot, channeltarget, "Duels devmode has been enabled in " + channeltarget + "!")
    elif command == 'off':
        if channeltarget not in duels_dev_channels:
            osd_notice(bot, instigator, "Duels devmode is already off in " + channel_current + ".")
            return
        adjust_database_array(bot, duelrecorduser, [channeltarget], 'devenabled', 'del')
        onscreentext(bot, channeltarget, "Duels devmode has been disabled in " + channeltarget + "!")
    else:
        osd_notice(bot, instigator, "Invalid command.")

## Health Subcommand
def duels_command_function_health(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    ## Build User Lists if not there already
    if botvisibleusers == []:
        botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)

    ## Get The Command Used
    healthcommand_list = ['healthpotion','stimpack']
    healthcommand = get_trigger_arg(bot, [x for x in command_restructure if x in healthcommand_list], 1) or 'view'

    ## Who is the target
    target = get_trigger_arg(bot, [x for x in command_restructure if x in botvisibleusers], 1) or instigator
    if target != instigator:
        validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
    target = actualname(bot, target)
    targetClass = get_database_value(bot, target, 'Class') or 'notClassy'
    targetrace = get_database_value(bot, target, 'race') or 'racist'

    if target != instigator and healthcommand in healthcommand_list:
        osd_notice(bot, instigator, "The health command for " + healthcommand + " is for self use only.")
        return

    ## View target/own health
    if healthcommand == 'view':
        
        ## Block viewing of other players inventories at lower levels
        if int(tiercommandeval) > int(currenttier) and target != instigator:
            if channel_current in duels_dev_channels or duel_admin_switch:
                allowpass = 1
            elif not channel_current.startswith("#") and len(duels_dev_channels) > 0:
                allowpass = 1
            else:
                osd_notice(bot, instigator, "Health for other players cannot be viewed until somebody reaches " + str(tierpepperrequired.title()) + ". "+str(tiermath) + " tier(s) remaining!")
                return
                
        ## Find Health of each limb, and display
        dispmsgarray = []
        totalhealth = 0
        totalhealthmax = 0
        targetClass = get_database_value(bot, target, 'Class') or 'notClassy'
        currenthealthtier = tierratio_level(bot)
        for x in stats_healthbodyparts:
            gethowmany = get_database_value(bot, target, x)
            gethowmanymax = array_compare(bot, x, stats_healthbodyparts, health_bodypart_max)
            gethowmanymax = gethowmanymax * currenthealthtier
            gethowmanymax = int(gethowmanymax)
            if gethowmany:
                xname = x.replace("_", " ")
                xname = xname.title()
                if targetrace == 'vampire':
                    gethowmany = -abs(gethowmany)
                    gethowmanymax = -abs(gethowmanymax)
                dispmsgarray.append(str(xname) + "=" + str(gethowmany) + "/" + str(gethowmanymax))
                totalhealth = totalhealth + gethowmany
                totalhealthmax = totalhealthmax + gethowmanymax
        dispmsgarrayb = []
        if dispmsgarray != []:
            dispmsgarrayb.append(target + "'s " + command_main + ":")
            dispmsgarrayb.append("Total Health=" + str(totalhealth)+ "/" + str(totalhealthmax))
            for y in dispmsgarray:
                dispmsgarrayb.append(y)
        else:
            dispmsgarrayb.append(instigator + ", It looks like " + target + " has no " +  command_main + ".")
        onscreentext(bot, ['say'], dispmsgarrayb)
        return

    ## How many of that item
    gethowmanylootitem = get_database_value(bot, instigator, healthcommand) or 0
    if not gethowmanylootitem:
        osd_notice(bot, instigator, "You do not have any " +  healthcommand + "!")
        return

    ## The quantity the player is applyint to this transaction
    quantity = get_trigger_arg(bot, [x for x in command_restructure if x == 'all' or str(x).isdigit()], 1) or 1
    if quantity == 'all':
        quantity = gethowmanylootitem

    ## Block for if the quantity above is greater than the players inventory
    if int(quantity) > int(gethowmanylootitem):
        osd_notice(bot, instigator, "You do not have enough " +  healthcommand + " to use this command! You only have " + str(gethowmanylootitem) + ".")
        return

    ## Class
    instigatorClass = get_database_value(bot, instigator, 'Class') or 'notClassy'
    instigatorrace = get_database_value(bot, instigator, 'race') or 'racist'
    
    if healthcommand == 'healthpotion':
        ## Dummy Vars
        mainlootusemessage,lootusedeaths= [],0

        ## Charge cost
        adjust_database_value(bot, instigator, 'healthpotion', -abs(quantity))

        ## Display based on quantity
        if int(quantity) == 1:
            mainlootusemessage.append(instigator + ' uses a healthpotion' + " Results: ")
        else:
            mainlootusemessage.append(instigator + ' uses ' + str(quantity) + " healthpotions. Results: ")

        ## Usage
        mainlootusemessage,lootusedeaths = use_loot_item(bot, instigator, instigator, instigatorClass, instigatorrace, 'healthpotion', quantity, mainlootusemessage, lootusedeaths)
        onscreentext(bot, channel_current, mainlootusemessage)
        return

    if healthcommand == 'stimpack':

        if instigatorrace == 'barbarian':
            potionmaths = int(quantity) * stimpack_worth_barbarian
        else:
            potionmaths = int(quantity) * stimpack_worth

        ## Select a body part
        bodypartselect = get_trigger_arg(bot, [x for x in command_restructure if x in stats_healthbodyparts], 1) or 'list'
        if bodypartselect not in stats_healthbodyparts:
            bodypartlist = get_trigger_arg(bot, stats_healthbodyparts, 'list')
            osd_notice(bot, instigator, "Select a valid body part to apply the stimpack to. Valid options: " + bodypartlist)
            return

        ## Health Maximum and status
        tierratio = tierratio_level(bot)
        maxbodyparthealth = array_compare(bot, bodypartselect, stats_healthbodyparts, health_bodypart_max)
        maxbodyparthealth = maxbodyparthealth * tierratio
        currentbodyparthealth = get_database_value(bot, instigator, bodypartselect)

        ## If already at max health. don't use
        if currentbodyparthealth >= maxbodyparthealth:
            osd_notice(bot, instigator, "It appears your " + bodypartselect + " is at max health.")
            return
            
        ## Sometimes if this isn't set, the game throws errors about strings or unicode
        quantity = int(quantity)

        ## Charge Cost and apply healing
        adjust_database_value(bot, instigator, 'stimpack', -abs(quantity))
        adjustmentamount = potionmaths * quantity
        adjust_database_value(bot, instigator, bodypartselect, adjustmentamount)

        ## Display results
        currentbodyparthealth = get_database_value(bot, instigator, bodypartselect)
        if currentbodyparthealth > maxbodyparthealth:
            set_database_value(bot, instigator, bodypartselect, maxbodyparthealth)
            currentbodyparthealth = maxbodyparthealth
        if currentbodyparthealth == maxbodyparthealth:
            onscreentext(bot, ['say'], instigator + " uses stimpack to heal " + bodypartselect + " to the maximum health of " + str(currentbodyparthealth) + ".")
        else:
            onscreentext(bot, ['say'], instigator + " uses stimpack to heal " + bodypartselect + " to " + str(currentbodyparthealth) + " health of the maximum " + str(maxbodyparthealth) + ".")
    return

## character SPECIAL
def duels_command_function_character(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    ## Build User Lists if not there already
    if botvisibleusers == []:
        botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)

    ## Who is the target
    target = get_trigger_arg(bot, [x for x in command_restructure if x in botvisibleusers], 1) or instigator
    if target != instigator:
        validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
    target = actualname(bot, target)
    targetClass = get_database_value(bot, target, 'Class') or 'notClassy'

    ## Block viewing of other players inventories at lower levels
    if int(tiercommandeval) > int(currenttier) and target != instigator:
        if channel_current in duels_dev_channels or duel_admin_switch:
            allowpass = 1
        elif not channel_current.startswith("#") and len(duels_dev_channels) > 0:
            allowpass = 1
        else:
            osd_notice(bot, instigator, "Special for other players cannot be viewed until somebody reaches " + str(tierpepperrequired.title()) + ". "+str(tiermath) + " tier(s) remaining!")
            return
            
    ## Find Health of each limb, and display
    dispmsgarray = []
    for x in stats_character:
        gethowmany = get_database_value(bot, target, x)
        if gethowmany:
            xname = xname.title()
            dispmsgarray.append(str(xname) + "=" + str(gethowmany))
    dispmsgarrayb = []
    if dispmsgarray != []:
        dispmsgarrayb.append(target + "'s SPECIAL stats:")
        for y in dispmsgarray:
            dispmsgarrayb.append(y)
    else:
        dispmsgarrayb.append(instigator + ", It looks like " + target + " has no SPECIAL Stats.")
    onscreentext(bot, ['say'], dispmsgarrayb)
    return

## Tier Subcommand
def duels_command_function_tier(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    command = get_trigger_arg(bot, triggerargsarray, 2)
    dispmsgarray = []
    currenttierpepper = pepper_tier(bot, currenttier)
    dispmsgarray.append("The current tier is " + str(currenttier)+ " ("+ str(currenttierpepper.title()) + ").")

    ## Display current/future features
    if not command:
        currenttierlistarray = []
        futuretierlistarray = []
        for i in range(0,16):
            tiercheck = eval("duels_commands_tier_unlocks_"+str(i))
            for x in tiercheck:
                if i <= currenttier:
                    currenttierlistarray.append(x)
                else:
                    futuretierlistarray.append(x)
        if currenttierlistarray != []:
            currenttierlist = get_trigger_arg(bot, currenttierlistarray, "list")
            dispmsgarray.append("Feature(s) currently available: " + currenttierlist + ".")
        if futuretierlistarray != []:
            futuretierlist = get_trigger_arg(bot, futuretierlistarray, "list")
            dispmsgarray.append("Feature(s) not yet unlocked: " + futuretierlist + ".")

    ## What tier is next
    elif command.lower() == 'next':
        nexttier = currenttier + 1
        if nexttier > 15:
            onscreentext(bot, channel_current, "Tiers do not got past 15 (Pure Capsaicin).")
            return
        nextpepper = pepper_tier(bot, nexttier)
        tiercheck = eval("duels_commands_tier_unlocks_"+str(nexttier))
        if tiercheck != []:
            tierlist = get_trigger_arg(bot, tiercheck, "list")
            dispmsgarray.append("Feature(s) that are available at tier " + str(nexttier) + " (" + str(nextpepper.title()) +"): " + tierlist + ".")
        else:
            dispmsgarray.append("No New Feature(s) available at tier " + str(nexttier) + " (" + str(nextpepper.title()) + ").")

    ## Find what tier a command is in
    elif command.lower() in commands_valid:
        commandtier = tier_command(bot, command)
        commandpepper = pepper_tier(bot, commandtier)
        dispmsgarray.append("The " + str(command) + " is unlocked at tier " + str(commandtier)+ " ("+ str(commandpepper.title()) + ").")
        tiercheck = eval("duels_commands_tier_unlocks_"+str(commandtier))
        tiermath = commandtier - currenttier
        if tiermath > 0:
            dispmsgarray.append(str(tiermath) + " tier(s) remaining!")

    ## find what tier a pepper level is
    elif command.lower() in duels_tier.pepper:
        commandtier = tier_pepper(bot, command)
        tiercheck = eval("duels_commands_tier_unlocks_"+str(commandtier))
        if tiercheck != []:
            tierlist = get_trigger_arg(bot, tiercheck, "list")
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
            onscreentext(bot, channel_current, "Tiers do not got past 15 (Pure Capsaicin).")
            return
        commandpepper = pepper_tier(bot, command)
        tiercheck = eval("duels_commands_tier_unlocks_"+str(command))
        if tiercheck != []:
            tierlist = get_trigger_arg(bot, tiercheck, "list")
            dispmsgarray.append("Feature(s) that are available at tier " + str(command) + " (" + str(commandpepper.title()) +"): " + tierlist + ".")
        else:
            dispmsgarray.append("No New Feature(s) available at tier " + str(command) + " (" + str(commandpepper.title()) + ").")
        tiermath = int(command) - currenttier
        if tiermath > 0:
            dispmsgarray.append(str(tiermath) + " tier(s) remaining!")

    ## find the player with the most xp, and how long until they reach a new tier
    elif command.lower() == 'closest':

        nexttier = currenttier + 1
        if int(nexttier) > 15:
            onscreentext(bot, channel_current, "Tiers do not got past 15 (Pure Capsaicin).")
            return
            
        playerarray,statvaluearray = [],[]
        for user in currentuserlistarray:
            statamount = get_database_value(bot, user, 'xp')
            if statamount > 0:
                playerarray.append(user)
                statvaluearray.append(statamount)

        if playerarray != [] and statvaluearray != []:
            statvaluearray, playerarray = array_arrangesort(bot, statvaluearray, playerarray)
            statleadername = get_trigger_arg(bot, playerarray, 'last')
            statleadernumber = get_trigger_arg(bot, statvaluearray, 'last')
            
            tierxprequired = get_trigger_arg(bot, duels_tier.xp, nexttier)
            tierxpmath = tierxprequired - statleadernumber
            dispmsgarray.append("The leader in xp is " + statleadername + " with " + str(statleadernumber) + ". The next tier is " + str(abs(tierxpmath)) + " xp away.")
            nextpepper = pepper_tier(bot, nexttier)
            tiercheck = eval("duels_commands_tier_unlocks_"+str(nexttier))
            if tiercheck != []:
                tierlist = get_trigger_arg(bot, tiercheck, "list")
                dispmsgarray.append("Feature(s) that are available at tier " + str(nexttier) + " (" + str(nextpepper.title()) +"): " + tierlist + ".")
            else:
                dispmsgarray.append("No New Feature(s) available at tier " + str(nexttier) + " (" + str(nextpepper.title()) + ").")
        else:
            dispmsgarray.append("Nobody is the closest to the next pepper level.")

    ## anything else is deemed a target, see what tier they are on if valid
    else:
        validtarget, validtargetmsg = targetcheck(bot, command, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
        targettier = get_database_value(bot, command, 'tier') or 0
        dispmsgarray.append(command + "'s current tier is " + str(targettier)+ ". ")

    ## display the info
    onscreentext(bot, ['say'], dispmsgarray)

## Suicide/harakiri
def duels_command_function_harakiri(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    ## Who is the target
    target = get_trigger_arg(bot, [x for x in command_restructure if x in botvisibleusers], 1) or instigator
    if target != instigator:
        validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
    target = actualname(bot, target)

    confirm = get_trigger_arg(bot, [x for x in command_restructure if x == 'confirm'], 1) or 0
    if not confirm:
        onscreentext(bot, channel_current, "You must run this command with 'confirm' to kill yourself. No rewards are given in to cowards.")
        return

    if target != instigator:
        if not duel_admin_switch:
            onscreentext(bot, channel_current, "You can't suicide other people. It's called Murder.")
            return

    suicidetextarray = suicidekill(bot,target)
    onscreentext(bot, ['say'], suicidetextarray)

## Russian Roulette
def duels_command_function_roulette(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    roulettesubcom = get_trigger_arg(bot, [x for x in command_restructure if x == 'last' or str(x).isdigit()], 1) or 'normal'

    if roulettesubcom == 'last':
        roulettelastplayeractual = get_database_value(bot, duelrecorduser, 'roulettelastplayeractualtext') or str("I don't have a record of the last roulette.")
        onscreentext(bot, channel_current, roulettelastplayeractual)
        return
    
    ## subcommands
    manualpick = 0
    if str(roulettesubcom).isdigit():
        if int(roulettesubcom) >= 1 and int(roulettesubcom) <= 6:
            manualpick = 1
        else:
            onscreentext(bot, channel_current, "Invalid Chamber Number!")
            return

    ## instigator must wait until the next round
    roulettelastshot = get_database_value(bot, duelrecorduser, 'roulettelastplayershot') or bot.nick
    if roulettelastshot == instigator:
        if channel_current in duels_dev_channels or duel_admin_switch:
            allowpass = 1
        elif not channel_current.startswith("#") and len(duels_dev_channels) > 0:
            allowpass = 1
        else:
            osd_notice(bot, instigator, "You must wait for the current round to complete, until you may play again.")
            return

    ## Instigator must wait a day after death
    getlastdeath = get_timesince_duels(bot, instigator, 'roulettedeath') or roulette_death_timeout
    if getlastdeath < roulette_death_timeout:
        if channel_current in duels_dev_channels or duel_admin_switch:
            allowpass = 1
        elif not channel_current.startswith("#") and len(duels_dev_channels) > 0:
            allowpass = 1
        else:
            osd_notice(bot, instigator, "You must wait 24 hours between roulette deaths.")
            return

    ## Small timeout
    getlastusage = get_timesince_duels(bot, duelrecorduser, str('lastfullroom' + command_main)) or timeout_roulette
    if getlastusage < timeout_roulette:
        if channel_current in duels_dev_channels or duel_admin_switch:
            allowpass = 1
        elif not channel_current.startswith("#") and len(duels_dev_channels) > 0:
            allowpass = 1
        else:
            osd_notice(bot, instigator, "Roulette has a small timeout.")
            return
    set_database_value(bot, duelrecorduser, str('lastfullroom' + command_main), now)

    ## Check who last pulled the trigger, or if it's a new chamber
    roulettelastplayer = get_database_value(bot, duelrecorduser, 'roulettelastplayer') or bot.nick
    roulettecount = get_database_value(bot, duelrecorduser, 'roulettecount') or 1

    ## Get the selected chamber from the database,, or set one
    roulettechamber = get_database_value(bot, duelrecorduser, 'roulettechamber')
    if not roulettechamber:
        roulettechamber = randint(1, 6)
        set_database_value(bot, duelrecorduser, 'roulettechamber', roulettechamber)

    ## Display Text
    instigatorcurse = get_database_value(bot, instigator, 'curse') or 0
    if manualpick == 1:
        onscreentext(bot, channel_current, instigator + " is blindfolded while the chamber is set to " + str(roulettesubcom) + ".")
    elif instigatorcurse:
        onscreentext(bot, channel_current, instigator + " spins the cylinder to the bullet's chamber and pulls the trigger.")
    elif roulettelastplayer == instigator and int(roulettecount) > 1:
        onscreentext(bot, channel_current, instigator + " spins the revolver and pulls the trigger.")
    elif int(roulettecount) == 1:
        onscreentext(bot, channel_current, instigator + " reloads the revolver, spins the cylinder and pulls the trigger.")
    else:
        onscreentext(bot, channel_current, instigator + " spins the cylinder and pulls the trigger.")

    ## Default 6 possible locations for bullet.
    ### curses
    if instigatorcurse:
        adjust_database_value(bot, instigator, 'curse', -1)
        reset_database_value(bot, duelrecorduser, 'roulettespinarray')
        currentspin = roulettechamber
    ## manual number
    elif manualpick == 1:
        currentspin = int(roulettesubcom)
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
            rouletteremove = get_trigger_arg(bot, roulettetemp, "random")
            roulettetempb = []
            roulettetempb.append(roulettechamber)
            for j in roulettetemp:
                if int(j) != int(rouletteremove):
                    roulettetempb.append(j)
            set_database_value(bot, duelrecorduser, 'roulettespinarray', roulettetempb)
            currentspin = get_trigger_arg(bot, roulettetempb, "random")
        else:
            currentspin = roulettechamber ## if only one location left
            reset_database_value(bot, duelrecorduser, 'roulettespinarray')
    else:
        roulettespinarray = [1,2,3,4,5,6]
        reset_database_value(bot, duelrecorduser, 'roulettespinarray')
        currentspin = get_trigger_arg(bot, roulettespinarray, "random")

    ### current spin is safe
    if int(currentspin) != int(roulettechamber):
        #time.sleep(randint(1, 3)) # added to build suspense
        onscreentext(bot, channel_current, "*click*")
        if manualpick == 1:
            roulettelastplayeractualtext = str(instigator + " manually picked a chamber without the bullet. The Bullet was moved.")
            onscreentext(bot, channel_current, instigator + " picked a chamber without the bullet. Bullet will be moved.")
            roulettechambernew = randint(1, 6)
            set_database_value(bot, duelrecorduser, 'roulettechamber', roulettechambernew)
        else:
            roulettelastplayeractualtext = str(instigator + " pulled the trigger and was safe.")
        roulettecount = roulettecount + 1
        roulettepayout = roulette_payout_default * roulettecount
        currentpayout = get_database_value(bot, instigator, 'roulettepayout')
        adjust_database_value(bot, instigator, 'roulettepayout', roulettepayout)
        set_database_value(bot, duelrecorduser, 'roulettecount', roulettecount)
        set_database_value(bot, duelrecorduser, 'roulettelastplayer', instigator)
        adjust_database_array(bot, duelrecorduser, [instigator], 'roulettewinners', 'add')

    ### instigator shoots themself in the head
    else:
        tierscaling = tierratio_level(bot)
        currenttierstart = get_database_value(bot, duelrecorduser, 'tier') or 0
        dispmsgarray = []

        if roulettecount == 1:
            if instigatorcurse:
                dispmsgarray.append("First in the chamber. Looks like " + instigator + " was cursed!")
            else:
                dispmsgarray.append("First in the chamber. What bad luck.")

        ## XP
        Classloser = get_database_value(bot, instigator, 'Class')
        losertier = get_database_value(bot, instigator, 'tier')
        if Classloser == 'ranger':
            XPearnedloser = xp_loser_ranger
        else:
            XPearnedloser = xp_loser
        if losertier < currenttierstart:
            XPearnedloser = XPearnedloser * tierscaling
        adjust_database_value(bot, instigator, 'xp', XPearnedloser)

        ## Dish out the pain
        damage = randint(50, 120)
        bodypart = 'head'
        revolver = get_trigger_arg(bot, roulette_revolver_list, 'random')
        damagescale = tierratio_level(bot)
        damage = damagescale * damage
        dispmsgarray.append(instigator + " shoots themself in the head with the " + revolver + ", dealing " + str(damage) + " damage. ")
        roulettelastplayeractualtext = str(instigator + " shot themself in the head with the " + revolver + ", dealing " + str(damage) + " damage. ")
        damage, damagetextarray = damage_resistance(bot, instigator, damage, bodypart)
        for x in damagetextarray:
            dispmsgarray.append(x)
        if damage > 0:
            adjust_database_value(bot, instigator, 'head', -abs(damage))
            instigatorcurrenthealth  = get_database_value(bot, instigator, 'head')
            if instigatorcurrenthealth  <= 0:
                suicidetextarray = suicidekill(bot,instigator)
                for x in suicidetextarray:
                    dispmsgarray.append(x)

        ## Payouts
        biggestpayout, biggestpayoutwinner = 0,''
        playerarray, statvaluearray = [],[]
        roulettewinners = get_database_value(bot, duelrecorduser, 'roulettewinners') or []
        uniquewinnersarray = []
        for x in roulettewinners:
            if x not in uniquewinnersarray and x != instigator:
                uniquewinnersarray.append(x)

        for x in uniquewinnersarray:

            ## Award XP
            Classwinner = get_database_value(bot, x, 'Class')
            winnertier = get_database_value(bot, x, 'tier')
            if Classwinner == 'ranger':
                XPearnedwinner = xp_winner_ranger
            else:
                XPearnedwinner = xp_winner
            if winnertier < currenttierstart:
                XPearnedwinner = XPearnedwinner * tierscaling
            adjust_database_value(bot, x, 'xp', XPearnedwinner)

            ## coin
            roulettepayoutx = get_database_value(bot, x, 'roulettepayout')
            if roulettepayoutx > 0:
                playerarray.append(x)
                statvaluearray.append(roulettepayoutx)
            adjust_database_value(bot, x, 'coin', roulettepayoutx)
            if roulettepayoutx > 0:
                osd_notice(bot, x, "Your roulette payouts = " + str(roulettepayoutx) + " coins!")
            reset_database_value(bot, x, 'roulettepayout')

        ## unique winner list
        if uniquewinnersarray != []:
            displaymessage = get_trigger_arg(bot, uniquewinnersarray, "list")
            if len(uniquewinnersarray) > 1:
                dispmsgarray.append("Winners: " + displaymessage + ".")
            else:
                dispmsgarray.append("Winner: " + displaymessage + ".")

        if playerarray != [] and statvaluearray != []:
            statvaluearray, playerarray = array_arrangesort(bot, statvaluearray, playerarray)
            statleadername = get_trigger_arg(bot, playerarray, 'last')
            statleadernumber = get_trigger_arg(bot, statvaluearray, 'last')
            dispmsgarray.append("Biggest Payout: "+ statleadername + " with " + str(statleadernumber) + " coins.")

        roulettecount = get_database_value(bot, duelrecorduser, 'roulettecount') or 1
        if roulettecount > 1:
            dispmsgarray.append("The chamber spun " + str(roulettecount) + " times. ")
        #time.sleep(randint(1, 2)) # added to build suspense
        onscreentext(bot, [channel_current], dispmsgarray)

        ## instigator must wait until the next round
        reset_database_value(bot, duelrecorduser, 'roulettelastplayershot')
        set_database_value(bot, duelrecorduser, 'roulettelastplayershot', instigator)

        ### Reset for next run
        reset_database_value(bot, duelrecorduser, 'roulettelastplayer')
        reset_database_value(bot, duelrecorduser, 'roulettechamber')
        reset_database_value(bot, duelrecorduser, 'roulettewinners')
        reset_database_value(bot, duelrecorduser, 'roulettecount')
        reset_database_value(bot, instigator, 'roulettepayout')
    set_database_value(bot, duelrecorduser, 'roulettelastplayeractualtext', roulettelastplayeractualtext)

## Assault
def duels_command_function_assault(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    if instigator in canduelarray:
        canduelarray.remove(instigator)
    displaymessage = get_trigger_arg(bot, canduelarray, "list")
    onscreentext(bot, channel_current, instigator + " Initiated a full channel " + command_main + " event. Good luck to " + displaymessage)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + command_main), now)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + command_main + 'instigator'), instigator)
    lastfoughtstart = get_database_value(bot, instigator, 'lastfought')
    for astat in assault_results:
        reset_database_value(bot, instigator, "assault_" + astat)
    for player in canduelarray:
        for astat in assault_results:
            reset_database_value(bot, player, "assault_" + astat)
    duel_combat(bot, instigator, instigator, canduelarray, triggerargsarray, now, channel_current, 'assault', duels_dev_channels, duels_enabled_channels, duel_admin_switch)
    maindueler = instigator
    osd_notice(bot, maindueler, "It looks like the Full Channel Assault has completed.")
    assaultstatsarray = []
    assaultstatsarray.append(maindueler + "'s Full Channel Assault results:")
    for astat in assault_results:
        astateval = get_database_value(bot, instigator, "assault_" + astat) or 0
        if astateval:
            astatstr = str(str(astat) + " = " + str(astateval))
            assaultstatsarray.append(astatstr)
            reset_database_value(bot, instigator, "assault_" + astat)
    onscreentext(bot, [channel_current], assaultstatsarray)
    for player in canduelarray:
        for astat in assault_results:
            reset_database_value(bot, player, "assault_" + astat)

    set_database_value(bot, instigator, 'lastfought', lastfoughtstart)

    ## usage counter ## TODO use len(canduelarray)
    adjust_database_value(bot, instigator, 'usage_total', 1)
    adjust_database_value(bot, instigator, 'usage_combat', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_total', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_combat', 1)

## Mayhem
def duels_command_function_mayhem(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    displaymessage = get_trigger_arg(bot, canduelarray, "list")
    onscreentext(bot, channel_current, instigator + " Initiated a full channel " + command_main + " event. Good luck to " + displaymessage)
    for user in canduelarray:
        for astat in assault_results:
            reset_database_value(bot, instigator, "assault_" + astat)

    ## Build second canduelarray
    mainduelerarray = []
    for userplayer in canduelarray:
        mainduelerarray.append(userplayer)
    random.shuffle(mainduelerarray)

    ## Every Player combination
    playercombinations = []
    for playercombo in itertools.product(mainduelerarray, canduelarray):
        playercombinations.append(playercombo)
    random.shuffle(playercombinations)
    for usercombo in playercombinations:
        currentcombo = []
        for combouser in usercombo:
            currentcombo.append(combouser)
        playera = get_trigger_arg(bot, currentcombo, 1)
        playerb = get_trigger_arg(bot, currentcombo, "last")
        if playera != playerb:
            playerafought = get_database_value(bot, playera, 'mayhemorganizer') or []
            playerbfought = get_database_value(bot, playerb, 'mayhemorganizer') or []
            if playera not in playerbfought and playerb not in playerafought:
                duel_combat(bot, instigator, playera, [playerb], triggerargsarray, now, channel_current, 'assault', duels_dev_channels, duels_enabled_channels, duel_admin_switch)
                adjust_database_array(bot, playera, playerb, 'mayhemorganizer', 'add')
                adjust_database_array(bot, playerb, playera, 'mayhemorganizer', 'add')

    ## Results
    for user in canduelarray:
        reset_database_value(bot, user, 'mayhemorganizer')
        assaultstatsarray = []
        assaultstatsarray.append(user + "'s Full Channel Mayhem results:")
        for astat in assault_results:
            astateval = get_database_value(bot, user, "assault_" + astat) or 0
            if astateval:
                astatstr = str(str(astat) + " = " + str(astateval))
                assaultstatsarray.append(astatstr)
                reset_database_value(bot, user, "assault_" + astat)
        if len(assaultstatsarray) > 1:
            onscreentext(bot, [channel_current], assaultstatsarray)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + command_main), now)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + command_main + 'instigator'), instigator)

## Hunger Games
def duels_command_function_hungergames(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    totaltributes = len(canduelarray)
    totaltributesstart = totaltributes
    if totaltributes == 1:
        osd_notice(bot, instigator, "There is only one tribute.  Try again later.")
        return
    currenttierstart = get_database_value(bot, duelrecorduser, 'tier') or 0
    tierscaling = tierratio_level(bot)
    dispmsgarray = []
    displaymessage = get_trigger_arg(bot, canduelarray, "list")
    onscreentext(bot, channel_current, instigator + " Initiated a full channel " + command_main + " event. Good luck to " + displaymessage)
    winnerorder = []
    while totaltributes > 0:
        totaltributes = totaltributes - 1
        winner = selectwinner(bot, canduelarray)
        winnerorder.append(winner)
        canduelarray.remove(winner)
    reversedorder = get_trigger_arg(bot, winnerorder, 'reverse')
    lastkilled = ''
    for player in reversedorder:
        if lastkilled != '':
            minidispmsgarray = []
            Classplayer = get_database_value(bot, player, 'Class') or 'notClassy'
            Classlastkilled = get_database_value(bot, lastkilled, 'Class') or 'notClassy'
            weapon = weaponofchoice(bot, player)
            weapon = weaponformatter(bot, weapon)
            minidispmsgarray.append(player + " hits " + lastkilled + " " + weapon + ', forcing a respawn.')
            whokilledwhom(bot, player, lastkilled)
            Classplayer = get_database_value(bot, player, 'Class')
            playertier = get_database_value(bot, player, 'tier')
            if Classplayer == 'ranger':
                XPearnedplayer = xp_winner_ranger
            else:
                XPearnedplayer = xp_winner
            if playertier < currenttierstart:
                XPearnedplayer = XPearnedplayer * tierscaling
            adjust_database_value(bot, player, 'xp', XPearnedplayer)
            Classlastkilled = get_database_value(bot, lastkilled, 'Class')
            lastkilledtier = get_database_value(bot, lastkilled, 'tier')
            if Classlastkilled == 'ranger':
                XPearnedlastkilled = xp_loser_ranger
            else:
                XPearnedlastkilled = xp_loser
            if lastkilledtier < currenttierstart:
                XPearnedlastkilled = XPearnedlastkilled * tierscaling
            adjust_database_value(bot, lastkilled, 'xp', XPearnedlastkilled)
            onscreentext(bot, [player,lastkilled], minidispmsgarray)
        else:
            dispmsgarray.append(player + " was the first to die.")
        lastkilled = player
    dispmsgarray.append(player + " is the victor!")
    reverseddisplay = get_trigger_arg(bot, dispmsgarray, 'reverse')
    onscreentext(bot, ['say'], reverseddisplay)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + command_main), now)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + command_main + 'instigator'), instigator)

## Colosseum
def duels_command_function_colosseum(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    if instigator in canduelarray:
        canduelarray.remove(instigator)
    currenttierstart = get_database_value(bot, duelrecorduser, 'tier') or 0
    tierscaling = tierratio_level(bot)
    dispmsgarray = []
    displaymessage = get_trigger_arg(bot, canduelarray, "list")
    onscreentext(bot, channel_current, instigator + " Initiated a full channel " + command_main + " event. Good luck to " + displaymessage)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + command_main), now)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + command_main + 'instigator'), instigator)
    totalplayers = len(canduelarray)
    riskcoins = int(totalplayers) * 30
    damage = riskcoins
    winner = selectwinner(bot, canduelarray)
    dispmsgarray.append("The Winner is: " + winner + "! Total winnings: " + str(riskcoins) + " coin! Losers took " + str(riskcoins) + " damage.")
    diedinbattle = []
    canduelarray.remove(winner)
    Classwinner = get_database_value(bot, winner, 'Class')
    winnertier = get_database_value(bot, winner, 'tier')
    if Classwinner == 'ranger':
        XPearnedwinner = xp_winner_ranger
    else:
        XPearnedwinner = xp_winner
    if winnertier < currenttierstart:
        XPearnedwinner = XPearnedwinner * tierscaling
    adjust_database_value(bot, winner, 'xp', XPearnedwinner)
    for x in canduelarray:
        Classloser = get_database_value(bot, x, 'Class')
        losertier = get_database_value(bot, x, 'tier')
        if Classloser == 'ranger':
            XPearnedloser = xp_loser_ranger
        else:
            XPearnedloser = xp_loser
        if losertier < currenttierstart:
            XPearnedloser = XPearnedloser * tierscaling
        adjust_database_value(bot, x, 'xp', XPearnedloser)
        damagescale = tierratio_level(bot)
        damage = damagescale * damage
        bodypart, bodypartname = bodypart_select(bot, x)
        damage, damagetextarray = damage_resistance(bot, x, damage, bodypart)
        for j in damagetextarray:
            dispmsgarray.append(j)
        if damage > 0:
            splitdamage = int(damage) / len(stats_healthbodyparts)
            for part in stats_healthbodyparts:
                adjust_database_value(bot, x, part, -abs(splitdamage))
            xheadhealth = get_database_value(bot, x, 'head')
            xtorsohealth = get_database_value(bot, x, 'torso')
            if xheadhealth  <= 0 or xtorsohealth <= 0:
                winnertextarray = whokilledwhom(bot, winner, x)
                diedinbattle.append(x)
            else:
                for part in stats_healthbodyparts:
                    xcurrenthealthbody  = get_database_value(bot, x, part)
                    if xcurrenthealthbody  <= 0:
                        if "_" in bodypartname:
                            bodypartname = bodypartname.replace("_", " ")
                        dispmsgarray.append(x + "'s " + bodypartname + " has become crippled!")
    if diedinbattle != []:
        displaymessage = get_trigger_arg(bot, diedinbattle, "list")
        dispmsgarray.append(displaymessage + " died in this event.")
    adjust_database_value(bot, winner, 'coin', riskcoins)
    onscreentext(bot, [channel_current], dispmsgarray)

## Quest
def duels_command_function_quest(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    displaymessage = get_trigger_arg(bot, canduelarray, "list")
    onscreentext(bot, channel_current, instigator + " Initiated a full channel " + command_main + " event. Good luck to " + displaymessage)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + command_main), now)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + command_main + 'instigator'), instigator)

    monsterstats(bot, currentduelplayersarray, 5)

    duel_combat(bot, instigator, 'duelsmonster', canduelarray, triggerargsarray, now, channel_current, 'quest', duels_dev_channels, duels_enabled_channels, duel_admin_switch)

    osd_notice(bot, instigator, "It looks like the Full Channel Quest has completed.")
    lastmonstername = get_database_value(bot, duelrecorduser, 'last_monster')

    assaultstatsarray = []
    assaultstatsarray.append("Full Channel Quest results (Monster was The " + lastmonstername + "):")
    for astat in assault_results:
        astateval = get_database_value(bot, 'duelsmonster', "assault_" + astat) or 0
        if astateval:
            astatstr = str(str(astat) + " = " + str(astateval))
            assaultstatsarray.append(astatstr)
            reset_database_value(bot, 'duelsmonster', "assault_" + astat)
    onscreentext(bot, [channel_current], assaultstatsarray)
    for player in canduelarray:
        for astat in assault_results:
            reset_database_value(bot, player, "assault_" + astat)

    refreshduelsmonster(bot)

## Monster
def duels_command_function_monster(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    monsterstats(bot, currentduelplayersarray, 1)
    duel_combat(bot, instigator, instigator, ['duelsmonster'], triggerargsarray, now, channel_current, 'combat', duels_dev_channels, duels_enabled_channels, duel_admin_switch)
    refreshduelsmonster(bot)

## Random Target
def duels_command_function_random(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    if canduelarray == []:
        osd_notice(bot, instigator, "It looks like the full channel " + command_main + " event target finder has failed.")
        return
    if bot.nick not in canduelarray:
        canduelarray.append(bot.nick)
    canduelarray.append('duelsmonster')
    target = get_trigger_arg(bot, canduelarray, 'random')
    if target == 'duelsmonster':
        monsterstats(bot, currentduelplayersarray, 1)
    else:
        statreset(bot, target)
    duel_combat(bot, instigator, instigator, [target], triggerargsarray, now, channel_current, 'random', duels_dev_channels, duels_enabled_channels, duel_admin_switch)
    if target == 'duelsmonster':
        refreshduelsmonster(bot)

## Usage
def duels_command_function_usage(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    targetcom = get_trigger_arg(bot, triggerargsarray, 2) or instigator
    targetcomname = targetcom
    if targetcom in commands_valid or targetcom == 'combat':
        target = get_trigger_arg(bot, triggerargsarray, 3) or instigator
        targetname = target
        if target == 'channel':
            target = bot.nick
        totaluses = get_database_value(bot, target, 'usage_'+targetcom)
        target = actualname(bot, target)
        onscreentext(bot, channel_current, targetname + " has used duel " + str(targetcom) + " " + str(totaluses) + " times.")
        return
    if targetcom == 'channel':
        targetcom = bot.nick
    validtarget, validtargetmsg = targetcheck(bot, targetcom, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
    if not validtarget and targetcom != bot.nick:
        osd_notice(bot, instigator, validtargetmsg)
        return
    totaluses = get_database_value(bot, targetcom, 'usage_total')
    targetcom = actualname(bot, targetcomname)
    onscreentext(bot, channel_current, targetcom + " has used duels " + str(totaluses) + " times.")

## War Room
def duels_command_function_warroom(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    subcommand = get_trigger_arg(bot, triggerargsarray, 2).lower()
    if not subcommand:
        if instigator not in canduelarray:
            canduel, validtargetmsg = duelcriteria(bot, instigator, subcommand, currentduelplayersarray, channel_current, duel_admin_switch)
            osd_notice(bot, instigator, validtargetmsg)
        else:
            osd_notice(bot, instigator, "It looks like you can duel.")
    elif subcommand == 'colosseum' or subcommand == 'assault':
        ## TODO new event types, maybe make an event array?
        ## TODO: alt commands
        executedueling, executeduelingmsg = eventchecks(bot, canduelarray, subcommand, instigator, currentduelplayersarray, channel_current,duel_admin_switch)
        if not executedueling:
            osd_notice(bot, instigator, executeduelingmsg)
        else:
            osd_notice(bot, instigator, "It looks like full channel " + subcommand + " event can be used.")
    elif subcommand == 'list':
        if instigator in canduelarray:
            canduelarray.remove(instigator)
        if bot.nick in canduelarray:
            canduelarray.remove(bot.nick)
        if canduelarray != []:
            displaymessage = get_trigger_arg(bot, canduelarray, "list")
            onscreentext(bot, channel_current, instigator + ", you may duel the following users: "+ str(displaymessage ))
        else:
            osd_notice(bot, instigator, "It looks like nobody can duel at the moment.")
    else:
        validtarget, validtargetmsg = targetcheck(bot, subcommand, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
        executedueling, executeduelingmsg = duelcriteria(bot, instigator, subcommand, currentduelplayersarray, channel_current, duel_admin_switch)
        if not executedueling:
            osd_notice(bot, instigator, executeduelingmsg)
            return
        subcommand = actualname(bot, subcommand)
        if subcommand in canduelarray and instigator in canduelarray:
            osd_notice(bot, instigator, "It looks like you can duel " + subcommand + ".")

## Title
def duels_command_function_title(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    instigatortitle = get_database_value(bot, instigator, 'title')
    titletoset = get_trigger_arg(bot, triggerargsarray, "2+")
    if not titletoset:
        osd_notice(bot, instigator, "What do you want your title to be?")
    elif titletoset == 'remove':
        reset_database_value(bot, instigator, 'title')
        osd_notice(bot, instigator, "Your title has been removed.")
    else:
        titletoset = str(titletoset)
        instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
        if instigatorcoin < title_cost:
            osd_notice(bot, instigator, "Changing your title costs " + str(title_cost) + " coin. You need more funding.")
        elif len(titletoset) > 10:
            osd_notice(bot, instigator, "Purchased titles can be no longer than 10 characters.")
        else:
            set_database_value(bot, instigator, 'title', titletoset)
            adjust_database_value(bot, instigator, 'coin', -abs(title_cost))
            osd_notice(bot, instigator, "Your title is now " + titletoset + ".")

## Streaks
def duels_command_function_streaks(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
    if int(tiercommandeval) > int(currenttier) and target != instigator:
        if channel_current in duels_dev_channels or duel_admin_switch:
            allowpass = 1
        elif not channel_current.startswith("#") and len(duels_dev_channels) > 0:
            allowpass = 1
        else:
            osd_notice(bot, instigator, "Streaks for other players cannot be viewed until somebody reaches " + str(tierpepperrequired.title()) + ". "+str(tiermath) + " tier(s) remaining!")
            return
    validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
    if not validtarget:
        osd_notice(bot, instigator, validtargetmsg)
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
def duels_command_function_stats(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
    if int(tiercommandeval) > int(currenttier) and target != instigator:
        if channel_current in duels_dev_channels or duel_admin_switch:
            allowpass = 1
        elif not channel_current.startswith("#") and len(duels_dev_channels) > 0:
            allowpass = 1
        else:
            osd_notice(bot, instigator, "Stats for other players cannot be viewed until somebody reaches " + str(tierpepperrequired.title()) + ". "+str(tiermath) + " tier(s) remaining!")
            return
    validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
    if not validtarget:
        osd_notice(bot, instigator, validtargetmsg)
        return
    target = actualname(bot, target)
    targetClass = get_database_value(bot, target, 'Class') or 'notClassy'
    targetrace = get_database_value(bot, target, 'race') or 'racist'
    dispmsgarray = []
    totalhealth = get_health(bot,target)
    if totalhealth:
        if targetrace == 'vampire':
            totalhealth = -abs(totalhealth)
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
            statname = x
            if statname == 'Class':
                statname = 'Class'
                gethowmany = gethowmany.title()
            statname = statname.title()
            dispmsgarray.append(statname + "=" + str(gethowmany))
    dispmsgarrayb = []
    if dispmsgarray != []:
        pepper = get_pepper(bot, target)
        if not pepper or pepper == '':
            targetname = target
        else:
            targetname = str("(" + str(pepper.title()) + ") " + target)
        dispmsgarrayb.append(targetname + "'s " + command_main + ":")
        for y in dispmsgarray:
            dispmsgarrayb.append(y)
    else:
        dispmsgarrayb.append(instigator + ", It looks like " + target + " has no " +  command_main + ".")
    onscreentext(bot, ['say'], dispmsgarrayb)

## Leaderboard
def duels_command_function_leaderboard(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    subcommand = get_trigger_arg(bot, triggerargsarray, 2)
    if bot.nick in currentduelplayersarray:
        currentduelplayersarray.remove(bot.nick)
    if not subcommand:
        leaderscript = []
        leaderboardarraystats = ['winlossratio','kills','respawns','health','streak_win_best','streak_loss_best','bounty']
        streak_loss_bestdispmsg, streak_loss_bestdispmsgb = "Worst Losing Streak:", ""
        winlossratiodispmsg, winlossratiodispmsgb = "Wins/Losses:", ""
        killsdispmsg, killsdispmsgb = "Most Kills:", "kills"
        respawnsdispmsg, respawnsdispmsgb = "Most Deaths:", "respawns"
        healthdispmsg, healthdispmsgb = "Closest To Death:", "health"
        streak_win_bestdispmsg, streak_win_bestdispmsgb = "Best Win Streak:", ""
        bountydispmsg, bountydispmsgb = "Largest Bounty:", "coins"
        for x in leaderboardarraystats:
            currentdispmsg = eval(x+"dispmsg")
            currentdispmsgb = eval(x+"dispmsgb")
            playerarray = []
            statvaluearray = []
            for u in currentduelplayersarray:
                if x != 'winlossratio' and x != 'health':
                    statamount = get_database_value(bot, u, x)
                else:
                    scriptdef = str('get_' + x + '(bot,u)')
                    statamount = eval(scriptdef)
                if statamount > 0:
                    playerarray.append(u)
                    statvaluearray.append(statamount)
            if playerarray != [] and statvaluearray != []:
                statvaluearray, playerarray = array_arrangesort(bot, statvaluearray, playerarray)
                if x == 'health':
                    statleadername = get_trigger_arg(bot, playerarray, 1)
                    statleadernumber = get_trigger_arg(bot, statvaluearray, 1)
                    leaderClass = get_database_value(bot, statleadername, 'Class') or 'notClassy'
                    leaderrace = get_database_value(bot, statleadername, 'race') or 'racist'
                    if leaderClass == 'vampire':
                        statleadernumber = int(statleadernumber)
                        statleadernumber = -abs(statleadernumber)
                elif x == 'winlossratio':
                    statleadername = get_trigger_arg(bot, playerarray, 'last')
                    statleadernumber = get_trigger_arg(bot, statvaluearray, 'last')
                    statleadernumber = format(statleadernumber, '.3f')
                else:
                    statleadername = get_trigger_arg(bot, playerarray, 'last')
                    statleadernumber = get_trigger_arg(bot, statvaluearray, 'last')
                leaderscript.append(str(currentdispmsg) + " " + str(statleadername) + " at " + str(statleadernumber) + " " + str(currentdispmsgb))
        if leaderscript == []:
            leaderscript.append("Leaderboard appears to be empty")
        onscreentext(bot, ['say'], leaderscript)
        return
    if subcommand.lower() != 'highest' and subcommand.lower() != 'lowest':
        osd_notice(bot, instigator, "Invalid Command.")
        return
    subcommand = subcommand.lower()
    subcommanda = get_trigger_arg(bot, triggerargsarray, 3)
    if not subcommanda:
        onscreentext(bot, channel_current, "What stat do you want to check?")
        return
    subcommanda = subcommanda.lower()
    duelstatsadminarray = duels_valid_stats(bot)
    if subcommanda.lower() not in duelstatsadminarray and subcommanda.lower() != 'health':
        onscreentext(bot, channel_current, "This stat is either not comparable at the moment or invalid.")
        return
    playerarray = []
    statvaluearray = []
    for u in currentduelplayersarray:
        if subcommanda.lower() != 'winlossratio' and subcommanda.lower() != 'health':
            statamount = get_database_value(bot, u, subcommanda.lower())
        else:
            scriptdef = str('get_' + subcommanda.lower() + '(bot,u)')
            statamount = eval(scriptdef)
        if statamount > 0:
            playerarray.append(u)
            statvaluearray.append(statamount)
    if playerarray != [] and statvaluearray != []:
        statvaluearray, playerarray = array_arrangesort(bot, statvaluearray, playerarray)
        if subcommand.lower() == 'lowest':
            statleadername = get_trigger_arg(bot, playerarray, 1)
            statleadernumber = get_trigger_arg(bot, statvaluearray, 1)
        else:
            statleadername = get_trigger_arg(bot, playerarray, 'last')
            statleadernumber = get_trigger_arg(bot, statvaluearray, 'last')
        if subcommanda.lower() == 'health':
            leaderClass = get_database_value(bot, statleadername, 'Class') or 'notClassy'
            leaderrace = get_database_value(bot, statleadername, 'race') or 'racist'
            if leaderClass == 'vampire':
                statleadernumber = int(statleadernumber)
                statleadernumber = -abs(statleadernumber)
        onscreentext(bot, channel_current, "The " + subcommand + " amount for "+ subcommanda+ " is " + statleadername+ " with "+ str(statleadernumber) + ".")
    else:
        onscreentext(bot, channel_current, "There doesn't appear to be a "+ subcommand + " amount for "+subcommanda+".")

## Armor
def duels_command_function_armor(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    subcommand = get_trigger_arg(bot, triggerargsarray, 2)
    typearmor = get_trigger_arg(bot, triggerargsarray, 3)
    instigatorClass = get_database_value(bot, instigator, 'Class')
    if not subcommand or subcommand.lower() in [x.lower() for x in dueloptedinarray]:
        target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
        validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
        target = actualname(bot, target)
        dispmsgarray = []
        for x in stats_armor:
            gethowmany = get_database_value(bot, target, x)
            if gethowmany:
                xname = x.replace("_", " ")
                xname = xname.title()
                if gethowmany > armor_durability:
                    xname = str("Enhanced " + xname)
                dispmsgarray.append(str(xname) + "=" + str(gethowmany))
        dispmsgarrayb = []
        if dispmsgarray != []:
            dispmsgarrayb.append(target + "'s " + command_main + " durability:")
            for y in dispmsgarray:
                dispmsgarrayb.append(y)
        else:
            dispmsgarrayb.append(instigator + ", It looks like " + target + " has no " +  command_main + ".")
        onscreentext(bot, ['say'], dispmsgarrayb)
    elif subcommand == 'buy':
        if typearmor != 'all':
            if not typearmor or typearmor not in stats_armor:
                armors = get_trigger_arg(bot, stats_armor, 'list')
                onscreentext(bot, channel_current, "What type of armor do you wish to " + subcommand + "? Options are: " + armors + ".")
                return
            getarmor = get_database_value(bot, instigator, typearmor) or 0
            if getarmor and getarmor > 0:
                onscreentext(bot, channel_current, "It looks like you already have a " + typearmor + ".")
                return
            armorcommandarray = [typearmor]
            costinvolved = armor_cost
        else:
            armorcommandarray = []
            for armor in stats_armor:
                getarmor = get_database_value(bot, instigator, armor) or 0
                if not getarmor or getarmor <= 0:
                    armorcommandarray.append(armor)
            costinvolved = armor_cost * len(armorcommandarray)
        if instigatorClass == 'blacksmith':
            costinvolved = costinvolved * armor_cost_blacksmith_cut
        costinvolved = int(costinvolved)
        instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
        if instigatorcoin < costinvolved:
            onscreentext(bot, channel_current, "Insufficient Funds.")
        else:
            onscreentext(bot, channel_current, instigator + " bought " + typearmor + " for " + str(costinvolved) + " coins.")
            adjust_database_value(bot, instigator, 'coin', -abs(costinvolved))
            for armorscom in armorcommandarray:
                set_database_value(bot, instigator, armorscom, armor_durability)
    elif subcommand == 'sell':
        if typearmor != 'all':
            if not typearmor or typearmor not in stats_armor:
                armors = get_trigger_arg(bot, stats_armor, 'list')
                onscreentext(bot, channel_current, "What type of armor do you wish to " + subcommand + "? Options are: " + armors + ".")
                return
            getarmor = get_database_value(bot, instigator, typearmor) or 0
            if not getarmor:
                onscreentext(bot, channel_current, "You don't have a " + typearmor + " to sell.")
                return
            if getarmor < 0:
                onscreentext(bot, channel_current, "Your armor is too damaged to sell.")
                reset_database_value(bot, instigator, typearmor)
                return
            armorcommandarray = [typearmor]
            durabilityremaining = getarmor / armor_durability
        else:
            armorcommandarray = []
            durabilityremaininga = 0
            for armor in stats_armor:
                getarmor = get_database_value(bot, instigator, armor) or 0
                if getarmor and getarmor > 0:
                    armorcommandarray.append(armor)
                    durabilityremaininga = getarmor + durabilityremaininga
            durabilityremainingmax = len(armorcommandarray) * armor_durability
            durabilityremaining = durabilityremaininga / durabilityremainingmax
        sellingamount = durabilityremaining * armor_cost
        if instigatorClass == 'blacksmith':
            sellingamount = sellingamount * armor_sell_blacksmith_cut
        sellingamount = int(sellingamount)
        onscreentext(bot, channel_current, "Selling " + typearmor +" armor earned you " + str(sellingamount) + " coins.")
        adjust_database_value(bot, instigator, 'coin', sellingamount)
        for armorscom in armorcommandarray:
            reset_database_value(bot, instigator, armorscom)
    elif subcommand == 'repair':
        if typearmor != 'all':
            if not typearmor or typearmor not in stats_armor:
                armors = get_trigger_arg(bot, stats_armor, 'list')
                onscreentext(bot, channel_current, "What type of armor do you wish to " + subcommand + "? Options are: " + armors + ".")
                return
            getarmor = get_database_value(bot, instigator, typearmor) or 0
            if not getarmor:
                onscreentext(bot, channel_current, "You don't have a " + typearmor + " to repair.")
                return
            durabilitycompare = armor_durability
            if instigatorClass == 'blacksmith':
                durabilitycompare = armor_durability_blacksmith
            if getarmor >= durabilitycompare:
                onscreentext(bot, channel_current, "It looks like your armor does not need repair.")
                return
            durabilitytorepair = durabilitycompare - getarmor
        else:
            armorcommandarray = []
            durabilityremaininga = 0
            for armor in stats_armor:
                getarmor = get_database_value(bot, instigator, armor) or 0
                if getarmor and getarmor > 0:
                    armorcommandarray.append(armor)
                    durabilityremaininga = getarmor + durabilityremaininga
            durabilitycompare = len(armorcommandarray) * armor_durability
            durabilitytorepair = durabilitycompare - durabilityremaininga
        instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
        costinvolved  = durabilitytorepair / durabilitycompare
        costinvolved = costinvolved * armor_cost
        costinvolved = costinvolved * armor_repair_cost
        if instigatorClass == 'blacksmith':
            costinvolved = costinvolved * armor_cost_blacksmith_cut
        costinvolved = int(costinvolved)
        if instigatorcoin < costinvolved:
            onscreentext(bot, channel_current, "Insufficient Funds.")
        else:
            onscreentext(bot, channel_current, "Repairing " + typearmor + " armor cost " + str(costinvolved)+" coins.")
            adjust_database_value(bot, instigator, 'coin', -abs(costinvolved))
            for armorscom in armorcommandarray:
                set_database_value(bot, instigator, armorscom, armor_durability)

## Bounty
def duels_command_function_bounty(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    target = get_trigger_arg(bot, triggerargsarray, 2)
    validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
    if not validtarget:
        osd_notice(bot, instigator, validtargetmsg)
        return
    target = actualname(bot, target)
    amount = get_trigger_arg(bot, triggerargsarray, 3)
    if not str(amount).isdigit():
        osd_notice(bot, instigator, "Invalid Amount.")
        return
    amount = int(amount)
    if not amount:
        osd_notice(bot, instigator, "How much of a bounty do you wish to place on "+target+".")
        return
    instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
    if int(instigatorcoin) < int(amount):
        osd_notice(bot, instigator, "Insufficient Funds.")
        return
    adjust_database_value(bot, instigator, 'coin', -abs(amount))
    bountyontarget = get_database_value(bot, target, 'bounty') or 0
    if not bountyontarget:
       onscreentext(bot, channel_current, instigator + " places a bounty of " + str(amount) + " on " + target + ".")
    else:
       onscreentext(bot, channel_current, instigator + " adds " + str(amount) + " to the bounty on " + target + ".")
    adjust_database_value(bot, target, 'bounty', amount)

## Deathblow
def duels_command_function_deathblow(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    deathblowtarget = get_database_value(bot, instigator, 'deathblowtarget')
    if not deathblowtarget:
        osd_notice(bot, instigator, "You don't have a deathblow target available.")
    else:
        deathblowtarget = actualname(bot,deathblowtarget)
        onscreentext(bot, channel_current, instigator + " strikes a deathblow upon " + deathblowtarget + ".")
        deathblowkilltext = whokilledwhom(bot, instigator, deathblowtarget) or ''
        onscreentext(bot, channel_current, deathblowkilltext)

## Grenade Command
def duels_command_function_grenade(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    if not channel_current.startswith("#"):
        osd_notice(bot, instigator, "Grenades must be used in channel.")
        return
    ## Build User Lists if not there already
    if botvisibleusers == []:
        botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)
    instigatorgrenade = get_database_value(bot, instigator, 'grenade') or 0
    if instigatorgrenade <= 0:
        osd_notice(bot, instigator, "You don't have a grenade to use!")
        return
    if instigator in canduelarray:
        canduelarray.remove(instigator)
    if bot.nick in canduelarray:
        canduelarray.remove(bot.nick)
    if canduelarray == []:
        osd_notice(bot, instigator, "It looks like using a grenade right now won't hurt anybody.")
    else:
        dispmsgarray = []
        adjust_database_value(bot, instigator, 'grenade', -1)
        fulltarget, secondarytarget, thirdtarget = '','',''
        fulltarget = get_trigger_arg(bot, canduelarray, "random")
        dispmsgarray.append(fulltarget + " takes the brunt of the grenade dealing " + str(abs(grenade_full_damage)) + " damage.")
        canduelarray.remove(fulltarget)
        if canduelarray != []:
            secondarytarget = get_trigger_arg(bot, canduelarray, "random")
            canduelarray.remove(secondarytarget)
            if canduelarray != []:
                thirdtarget = get_trigger_arg(bot, canduelarray, "random")
                dispmsgarray.append(secondarytarget + " and " + thirdtarget + " jump away but still take " + str(abs(grenade_secondary_damage)) + " damage.")
                canduelarray.remove(thirdtarget)
                if canduelarray != []:
                    remainingarray = get_trigger_arg(bot, canduelarray, "list")
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
            bodypart, bodypartname = bodypart_select(bot, player)
            damage, damagetextarray = damage_resistance(bot, player, damage, bodypart)
            for j in damagetextarray:
                dispmsgarray.append(j)
            if damage > 0:
                splitdamage = int(damage) / len(stats_healthbodyparts)
                for part in stats_healthbodyparts:
                    adjust_database_value(bot, player, part, -abs(splitdamage))
                playerheadhealth = get_database_value(bot, player, 'head')
                playertorsohealth = get_database_value(bot, player, 'torso')
                if playerheadhealth  <= 0 or playertorsohealth <= 0:
                    winnertextarray = whokilledwhom(bot, instigator, player)
                    diedinbattle.append(player)
                else:
                    for part in stats_healthbodyparts:
                        playercurrenthealthbody  = get_database_value(bot, player, part)
                        if playercurrenthealthbody  <= 0:
                            bodypartname = bodypartname.replace("_", " ")
                            dispmsgarray.append(player + "'s " + bodypartname + " has become crippled!")
        if diedinbattle != []:
            displaymessage = get_trigger_arg(bot, diedinbattle, "list")
            dispmsgarray.append(displaymessage + " died by this grenade volley.")
        onscreentext(bot, [channel_current], dispmsgarray)

## Loot
def duels_command_function_loot(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    ## Build User Lists if not there already
    if botvisibleusers == []:
        botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)
        
    instigatorClass = get_database_value(bot, instigator, 'Class')
    instigatorcoin = get_database_value(bot, instigator, 'coin') or 0

    ## Get The Command Used
    lootcommand = get_trigger_arg(bot, [x for x in command_restructure if x in loot_transaction_types], 1) or 'view'

    ## Who is the target
    target = get_trigger_arg(bot, [x for x in command_restructure if x in botvisibleusers], 1) or instigator
    if target != instigator:
        validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
    target = actualname(bot, target)
    targetClass = get_database_value(bot, target, 'Class') or 'notClassy'
    targetrace = get_database_value(bot, target, 'race') or 'racist'

    ## IF not just viewing
    if lootcommand in loot_transaction_types:

        ## Main transaction item
        lootitem = get_trigger_arg(bot, [x for x in command_restructure if x in loot_all_types], 1)
        if not lootitem:
            osd_notice(bot, instigator, "What do you want to " + str(lootcommand) + "?")
            return

        ## How many of that item
        gethowmanylootitem = get_database_value(bot, instigator, lootitem) or 0
        if not gethowmanylootitem and lootcommand != 'buy':
            osd_notice(bot, instigator, "You do not have any " +  lootitem + "!")
            return

        ## The quantity the player is applyint to this transaction
        quantity = get_trigger_arg(bot, [x for x in command_restructure if x == 'all' or str(x).isdigit()], 1) or 1
        if lootcommand != 'trade':
            if quantity == 'all':
                quantity = gethowmanylootitem

            ## Block for if the quantity above is greater than the players inventory
            if int(quantity) > int(gethowmanylootitem) and lootcommand != 'buy':
                osd_notice(bot, instigator, "You do not have enough " +  lootitem + " to use this command! You only have " + str(gethowmanylootitem) + ".")
                return
            
        ## Magicpotions are only tradeable, other transactions are blocked
        if lootitem == 'magicpotion' and lootcommand != 'trade':
            osd_notice(bot, instigator, "Magic Potions are not purchasable, sellable, or usable. They can only be traded.")
            return

    ## View target/own inventory
    if lootcommand == 'view':
        
        ## Block viewing of other players inventories at lower levels
        if int(tiercommandeval) > int(currenttier) and target != instigator:
            if channel_current in duels_dev_channels or duel_admin_switch:
                allowpass = 1
            elif not channel_current.startswith("#") and len(duels_dev_channels) > 0:
                allowpass = 1
            else:
                osd_notice(bot, instigator, "Loot for other players cannot be viewed until somebody reaches " + str(tierpepperrequired.title()) + ". "+str(tiermath) + " tier(s) remaining!")
                return

        ## Process quantities of items in inventory
        dispmsgarray = []
        for x in loot_view:
            gethowmany = get_database_value(bot, target, x)
            if gethowmany:
                xname = x.title()
                if gethowmany == 1:
                    loottype = str(xname)
                else:
                    loottype = str(str(xname)+"s")
                dispmsgarray.append(str(loottype) + "=" + str(gethowmany))

        ## Display above info
        dispmsgarrayb = []
        if dispmsgarray != []:
            dispmsgarrayb.append(target + "'s " + command_main + ":")
            for y in dispmsgarray:
                dispmsgarrayb.append(y)
        else:
            dispmsgarrayb.append(instigator + ", It looks like " + target + " has no " +  command_main + ".")
        onscreentext(bot, ['say'], dispmsgarrayb)

    ## Player intends to use item
    elif lootcommand == 'use':

        ## Stimpacks are only usable via the health command
        if lootitem == 'stimpack':
            osd_notice(bot, instigator, "This is currently only avaliable by running .duel health stimpack .")

        ## Redirect to the grenade command
        elif lootitem == 'grenade':
            duels_command_function_grenade(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, command_restructure, command_restructure)
            return

        ## Timepotions are no good in quantities over 1
        if lootitem == 'timepotion':
            quantity = 1

        ## Sometimes if this isn't set, the game throws errors about strings or unicode
        quantity = int(quantity)
        
        ## charge the cost
        adjust_database_value(bot, instigator, lootitem, -abs(quantity))
        
        ## fiends are immune to being targeted with potions
        if target.lower() != instigator.lower() and targetrace == 'fiend':
            osd_notice(bot, instigator, "It looks like " + target + " is a fiend and can only self-use potions. This actions still costs you.")
            return

        ## Empty settings
        lootusedeaths = 0
        mainlootusemessage,uselootarray,extramsg = [],[],[]

        ## Display based on target and quantity
        if target == instigator:
            if int(quantity) == 1:
                mainlootusemessage.append(instigator + ' uses a ' + lootitem + ". Results: ")
            else:
                mainlootusemessage.append(instigator + ' uses ' + str(quantity) + " " + lootitem + 's' + ". Results: ")
        else:
            if int(quantity) == 1:
                mainlootusemessage.append(instigator + ' uses a' + lootitem + ' on ' + target + ". Results: ")
            else:
                mainlootusemessage.append(instigator + " used " + str(quantity) + " " + lootitem + "s on " + target + ". Results: ")

        ## If not mysterypotion, apply the potion quickly
        if lootitem != 'mysterypotion':
            mainlootusemessage,lootusedeaths = use_loot_item(bot, instigator, target, targetClass, targetrace, lootitem, quantity, mainlootusemessage, lootusedeaths)
        else:

            ## Build a list of potions, randomly
            while int(quantity) > 0:
                quantity = int(quantity) - 1
                loot = get_trigger_arg(bot, potion_types, 'random')
                if loot == 'mysterypotion' or loot == 'magicpotion':
                    loot = get_trigger_arg(bot, loot_null, 'random')
                uselootarray.append(loot)

            ## Build baseline of how we will display what potions were used
            actualpotionmathedarray = []
            alreadyprocessedarray = []
            healthpotion_quantity,manapotion_quantity,poisonpotion_quantity,timepotion_quantity,staminapotion_quantity = 0,0,0,0,0
            for fluid in uselootarray:
                if fluid not in alreadyprocessedarray:
                    alreadyprocessedarray.append(fluid)
                    countedeval = uselootarray.count(fluid)
                    if countedeval > 1:
                       actualpotionmathedarray.append(str(str(countedeval) + " "+fluid + "s"))
                    else:
                        actualpotionmathedarray.append(fluid)
                    if fluid in potion_types:
                        if fluid == 'healthpotion':
                            healthpotion_quantity = healthpotion_quantity + countedeval
                        elif fluid == 'manapotion':
                            manapotion_quantity = manapotion_quantity + countedeval
                        elif fluid == 'poisonpotion':
                            poisonpotion_quantity = poisonpotion_quantity + countedeval
                        elif fluid == 'timepotion':
                            timepotion_quantity = 1
                        elif fluid == 'staminapotion':
                            staminapotion_quantity = staminapotion_quantity + countedeval
            postionsusedarray = get_trigger_arg(bot, actualpotionmathedarray, "list")
            mainlootusemessage.append("Potion(s) used: " + postionsusedarray + ". Results: ")

            ## Actual Usage
            for potiontype in potion_types:
                if potiontype != 'mysterypotion' and potiontype != 'magicpotion':
                    quantitytouse = eval(potiontype+"_quantity")
                    if quantitytouse > 0:
                        mainlootusemessage,lootusedeaths = use_loot_item(bot, instigator, target, targetClass, targetrace, potiontype, quantitytouse, mainlootusemessage, lootusedeaths)

        ## Display if this action caused death
        if lootusedeaths > 0:
            if lootusedeaths == 1:
                mainlootusemessage.append("This resulted in death.")
            else:
                mainlootusemessage.append("This resulted in "+str(lootusedeaths)+" deaths.")

        ## Display to player/target in privmsg if command issued in privmsg, otherwise in channel
        onscreentext(bot, channel_current, mainlootusemessage)
        if target != instigator and not channel_current.startswith("#"):
            osd_notice(bot, target, mainlootusemessage)

    ## Buying
    elif lootcommand == 'buy':

        ## Sometimes if this isn't set, the game throws errors about strings or unicode
        quantity = int(quantity)

        ## Scavengers have a lower cost
        if instigatorClass == 'scavenger':
            coinrequired = loot_buy_scavenger * int(quantity)

        ## Normal Cost
        else:
            coinrequired = loot_buy * int(quantity)

        ## Block transaction if player doesn not have enough coin
        if int(instigatorcoin) < coinrequired:
            osd_notice(bot, instigator, "You do not have enough coin for this action.")
            return

        ## Apply cost, adjust inventory, and display accordingly
        adjust_database_value(bot, instigator, 'coin', -abs(coinrequired))
        adjust_database_value(bot, instigator, lootitem, quantity)
        onscreentext(bot, instigator, instigator + " bought " + str(quantity) +  " "+lootitem + "s for " +str(coinrequired)+ " coins.")

    ##  Selling lootitem
    elif lootcommand == 'sell':

        ## Sometimes if this isn't set, the game throws errors about strings or unicode
        quantity = int(quantity)

        ## Scavengers make more money when selling
        if instigatorClass == 'scavenger':
            reward = loot_sell_scavenger * int(quantity)
        else:
            reward = loot_sell * int(quantity)

        ## Apply payment, adjust inventory, and display accordingly
        adjust_database_value(bot, instigator, 'coin', reward)
        adjust_database_value(bot, instigator, lootitem, -abs(quantity))
        onscreentext(bot, channel_current, instigator + " sold " + str(quantity) + " "+ lootitem + "s for " +str(reward)+ " coins.")

    ## Trading system
    elif lootcommand == 'trade':

        ## What is the second loot item, that is being traded for
        lootitemb = get_trigger_arg(bot, [x for x in command_restructure if x in loot_all_types], 2)
        if not lootitemb:
            osd_notice(bot, instigator, "What do you want to " + str(lootcommand) + "?")
            return

        ## Grenade block
        if lootitem == 'grenade' or lootitemb == 'grenade':
            osd_notice(bot, instigator, "You can't trade for grenades.")
            return

        ## Stimpack block
        if lootitem == 'stimpack' or lootitemb == 'stimpack':
            osd_notice(bot, instigator, "You can't trade for stimpacks.")
            return

        ## Cannot trade for the same item
        elif lootitemb == lootitem:
            osd_notice(bot, instigator, "You can't trade for the same type of potion.")
            return

        ## Trading ratios, scavengers have a better ratio, magicpotions are always 1:1
        if lootitem == 'magicpotion':
            tradingratio = 1
        elif instigatorClass == 'scavenger':
            tradingratio = loot_trade_scavenger
        else:
            tradingratio = loot_trade

        ## validate Quantity
        if quantity == 'all':
            quantity = gethowmanylootitem / tradingratio
        if quantity <= 0:
            osd_notice(bot, instigator, "You do not have enough "+lootitem+" for this action.")
            return
        quantitymath = tradingratio * int(quantity)
        if gethowmanylootitem < quantitymath:
            osd_notice(bot, instigator, "You don't have enough of this item to trade.")
            return

        ## Sometimes if this isn't set, the game throws errors about strings or unicode
        quantity = int(quantity)

        ## adjust inventory, and display accordingly
        adjust_database_value(bot, instigator, lootitem, -abs(quantitymath))
        adjust_database_value(bot, instigator, lootitemb, quantity)
        onscreentext(bot, channel_current, instigator + " traded " + str(quantitymath) + " "+ lootitem + "s for " +str(quantity) + " "+ lootitemb+ "s.")

## Weaponslocker ## TODO
def duels_command_function_weaponslocker(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
    validdirectionarray = ['total','inv','add','del','reset']
    if target in validdirectionarray:
        target = instigator
        adjustmentdirection = get_trigger_arg(bot, triggerargsarray, 2).lower()
        weaponchange = get_trigger_arg(bot, triggerargsarray, '3+')
    else:
        adjustmentdirection = get_trigger_arg(bot, triggerargsarray, 3).lower()
        weaponchange = get_trigger_arg(bot, triggerargsarray, '4+')
    weaponslist = get_database_value(bot, target, 'weaponslocker_complete') or []
    validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
    if not validtarget:
        osd_notice(bot, instigator, validtargetmsg)
        return
    target = actualname(bot, target)
    if not adjustmentdirection:
        osd_notice(bot, instigator, "Use .duel weaponslocker add/del to adjust Locker Inventory.")
    elif adjustmentdirection == 'total':
        gethowmany = get_database_array_total(bot, target, 'weaponslocker_complete')
        onscreentext(bot, channel_current, target + ' has ' + str(gethowmany) + " weapons in their locker. They Can be viewed in privmsg by running .duel weaponslocker inv .")
    elif adjustmentdirection == 'inv':
        if weaponslist == []:
            osd_notice(bot, instigator, "There doesnt appear to be anything in the weapons locker! Use .duel weaponslocker add/del to adjust Locker Inventory.")
            return
        howmanyweapons = len(weaponslist)
        weaponsonscreenarray = []
        for weapon in weaponslist:
            howmanyweapons = howmanyweapons - 1
            if howmanyweapons > 0:
                weapon = str(weapon+",")
            weaponsonscreenarray.append(weapon)
        onscreentext(bot, [instigator], weaponsonscreenarray)
    elif target != instigator and not duel_admin_switch:
        osd_notice(bot, instigator, "You may not adjust somebody elses locker.")
    elif adjustmentdirection == 'reset':
        reset_database_value(bot, target, 'weaponslocker_complete')
        osd_notice(bot, instigator, "Locker Reset.")
    else:
        if not weaponchange:
            osd_notice(bot, instigator, "What weapon would you like to add/remove?")
        elif adjustmentdirection != 'add' and adjustmentdirection != 'del':
            onscreentext(bot, channel_current, "Invalid Command.")
        elif adjustmentdirection == 'add' and weaponchange in weaponslist:
            osd_notice(bot, instigator, weaponchange + " is already in weapons locker.")
        elif adjustmentdirection == 'del' and weaponchange not in weaponslist:
            osd_notice(bot, instigator, weaponchange + " is already not in weapons locker.")
        elif adjustmentdirection == 'add' and len(weaponchange) > weapon_name_length:
            osd_notice(bot, instigator, "That weapon exceeds the character limit of "+str(weapon_name_length)+".")
        else:
            if adjustmentdirection == 'add':
                weaponlockerstatus = 'now'
            else:
                weaponlockerstatus = 'no longer'
            adjust_database_array(bot, target, [weaponchange], 'weaponslocker_complete', adjustmentdirection)
            message = str(weaponchange + " is " + weaponlockerstatus + " in weapons locker.")
            osd_notice(bot, instigator, message)

## Magic ## TODO
def duels_command_function_magic(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):
    instigatorClass = get_database_value(bot, instigator, 'Class')
    instigatormana = get_database_value(bot, instigator, 'mana')
    magicusage = get_trigger_arg(bot, triggerargsarray, 2)
    if not magicusage or magicusage not in magic_types:
        magicoptions = get_trigger_arg(bot, magic_types, 'list')
        onscreentext(bot, channel_current, "Magic uses include: " + magicoptions + ".")
    else:
        targnum = get_trigger_arg(bot, triggerargsarray, 3).lower()
        if not targnum:
            quantity = 1
            target = instigator
        elif targnum.isdigit():
            quantity = int(targnum)
            target = instigator
        elif targnum.lower() in [x.lower() for x in dueloptedinarray]:
            targnumb = get_trigger_arg(bot, triggerargsarray, 4).lower()
            target = targnum
            if not targnumb:
                quantity = 1
            elif targnumb.isdigit():
                quantity = int(targnumb)
            elif targnumb == 'all':
                quantity = int(gethowmanylootitem)
            else:
                onscreentext(bot, channel_current, "Invalid command.")
                return
        if not instigatormana:
            osd_notice(bot, instigator, "You don't have any mana.")
            return
        validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
        if target == bot.nick:
            osd_notice(bot, instigator, "I am immune to magic " + magicusage + ".")
            return
        target = actualname(bot, target)
        targetClass = get_database_value(bot, target, 'Class') or 'notClassy'
        targetrace = get_database_value(bot, target, 'race') or 'racist'
        if target.lower() != instigator.lower() and targetrace == 'fiend':
            osd_notice(bot, instigator, "It looks like " + target + " is a fiend and can only self-use magic.")
            manarequired = -abs(manarequired)
            adjust_database_value(bot, instigator, 'mana', manarequired)
            return
        targetcurse = get_database_value(bot, target, 'curse') or 0
        if magicusage == 'curse' and targetcurse:
            osd_notice(bot, instigator, "It looks like " + target + " is already cursed.")
            return
        if magicusage == 'curse':
            manarequired = magic_mana_required_curse
        elif magicusage == 'shield':
            manarequired = magic_mana_required_shield
        else:
            return
        if instigatorClass == 'mage':
            manarequired = manarequired * magic_usage_mage
        actualmanarequired = int(manarequired) * int(quantity)
        if int(actualmanarequired) > int(instigatormana):
            manamath = int(int(actualmanarequired) - int(instigatormana))
            osd_notice(bot, instigator, "You need " + str(manamath) + " more mana to use magic " + magicusage + ".")
        else:
            specialtext = ''
            manarequired = -abs(actualmanarequired)
            adjust_database_value(bot, instigator, 'mana', manarequired)
            if magicusage == 'curse':
                damagedealt = magic_curse_damage * int(quantity)
                set_database_value(bot, target, 'curse', magic_curse_duration)
                specialtext = str("which forces " + target + " to lose the next " + str(magic_curse_duration) + " duels.")
                splitdamage = int(damagedealt) / len(stats_healthbodyparts)
                for part in stats_healthbodyparts:
                    adjust_database_value(bot, target, part, -abs(splitdamage))
            elif magicusage == 'shield':
                damagedealt = magic_shield_health * int(quantity)
                actualshieldduration = int(quantity) * int(magic_shield_duration)
                adjust_database_value(bot, target, 'shield', actualshieldduration)
                specialtext = str("which allows " + target + " to take no damage for the duration of " + str(actualshieldduration) + " damage AND restoring " +str(abs(damagedealt)) + " health.")
                splitdamage = int(damagedealt) / len(stats_healthbodyparts)
                for part in stats_healthbodyparts:
                    adjust_database_value(bot, target, part, splitdamage)
            if instigator == target:
                displaymsg = str(instigator + " uses magic " + magicusage + " " + specialtext + ".")
            else:
                displaymsg = str(instigator + " uses magic " + magicusage + " on " + target + " " + specialtext + ".")
            onscreentext(bot, channel_current, displaymsg)
            if not channel_current.startswith("#") and target != instigator:
                osd_notice(bot, instigator, displaymsg)
            instigatormana = get_database_value(bot, instigator, 'mana')
            if instigatormana <= 0:
                reset_database_value(bot, instigator, 'mana')

## Admin ## TODO
def duels_command_function_admin(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, command_main, now, trigger, currenttier, channel_current, currentduelplayersarray, canduelarray, command_full , tiercommandeval, tierpepperrequired, tiermath, duels_dev_channels, commands_valid, duels_enabled_channels, duel_admin_switch, command_restructure):

    ## Build User Lists if not there already
    if botvisibleusers == []:
        botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray = users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch)

    subcommand = get_trigger_arg(bot, triggerargsarray, 2).lower()
    if subcommand not in commands_valid and subcommand != 'bugbounty' and subcommand != 'channel':
        osd_notice(bot, instigator, "What Admin adjustment do you want to make?")
        return
    if subcommand == 'on' or subcommand == 'off':
        target = get_trigger_arg(bot, triggerargsarray, 3).lower() or instigator
        if target == 'everyone':
            if subcommand == 'on':
                adjust_database_array(bot, duelrecorduser, botvisibleusers, 'duelusers', 'add')
            else:
                reset_database_value(bot, duelrecorduser, 'duelusers')
            osd_notice(bot, instigator, "Duels should now be " +  subcommand + ' for ' + target +".")
            return
        if subcommand == 'on':
            adjust_database_array(bot, duelrecorduser, [target], 'duelusers', 'add')
        else:
            adjust_database_array(bot, duelrecorduser, [target], 'duelusers', 'del')
        set_database_value(bot, target, 'timeout_opttime', now)
        osd_notice(bot, instigator, "Duels should now be " +  subcommand + ' for ' + target +".")
    elif subcommand == 'tier':
        command = get_trigger_arg(bot, triggerargsarray, 3).lower()
        if not command:
            osd_notice(bot, instigator, "What did you intend to do with tiers?")
            return
        target = get_trigger_arg(bot, triggerargsarray, 4).lower() or instigator
        if target == 'channel':
            target = duelrecorduser
        if command == 'view':
            viewedtier = get_database_value(bot, target, 'tier')
            osd_notice(bot, instigator, target + " is at tier " + str(viewedtier) + ".")
        elif command == 'reset':
            osd_notice(bot, instigator, target + "'s tier has been reset.")
            reset_database_value(bot, target, 'tier')
        elif command == 'set':
            newsetting = get_trigger_arg(bot, triggerargsarray, 5)
            if not newsetting or not newsetting.isdigit():
                osd_notice(bot, instigator, "You must specify a number setting.")
                return
            osd_notice(bot, instigator, target + "'s tier has been set to " + str(newsetting) + ".")
            set_database_value(bot, target, 'tier', int(newsetting))
        else:
            osd_notice(bot, instigator, "This looks to be an invalid command.")
    elif subcommand == 'bugbounty':
        target = get_trigger_arg(bot, triggerargsarray, 3).lower() or instigator
        onscreentext(bot, channel_current, target + ' is awarded ' + str(bugbounty_reward) + " coin for finding a bug in duels.")
        adjust_database_value(bot, target, 'coin', bugbounty_reward)
    elif subcommand == 'roulette':
        command = get_trigger_arg(bot, triggerargsarray, 3).lower()
        if command != 'reset':
            osd_notice(bot, instigator, "What did you intend to do with roulette?")
            return
        osd_notice(bot, instigator, "Roulette should now be reset.")
        reset_database_value(bot, duelrecorduser, 'roulettelastplayer')
        reset_database_value(bot, duelrecorduser, 'roulettechamber')
        reset_database_value(bot, duelrecorduser, 'roulettewinners')
        reset_database_value(bot, duelrecorduser, 'roulettecount')
        reset_database_value(bot, duelrecorduser, 'roulettespinarray')
        for user in botvisibleusers:
            reset_database_value(bot, user, 'roulettepayout')
    elif subcommand == 'stats':
        incorrectdisplay = "A correct command use is .duel admin stats target set/reset stat."
        target = get_trigger_arg(bot, triggerargsarray, 3)
        subcommand = get_trigger_arg(bot, triggerargsarray, 4)
        statset = get_trigger_arg(bot, triggerargsarray, 5)
        newvalue = get_trigger_arg(bot, triggerargsarray, 6)
        duelstatsadminarray = duels_valid_stats(bot)
        if not target:
            osd_notice(bot, instigator, "Target Missing. " + incorrectdisplay)
        elif target.lower() not in [u.lower() for u in botvisibleusers] and target != 'everyone':
            osd_notice(bot, instigator, "It looks like " + str(target) + " is either not here, or not a valid person.")
        elif not subcommand:
            osd_notice(bot, instigator, "Subcommand Missing. " + incorrectdisplay)
        elif subcommand not in stat_admin_commands:
            osd_notice(bot, instigator, "Invalid subcommand. " + incorrectdisplay)
        elif not statset:
            osd_notice(bot, instigator, "Stat Missing. " + incorrectdisplay)
        elif statset not in duelstatsadminarray and statset != 'all':
            osd_notice(bot, instigator, "Invalid stat. " + incorrectdisplay)
        else:
            target = actualname(bot, target)
            if subcommand == 'reset':
                newvalue = None
            if subcommand == 'set' and newvalue == None:
                osd_notice(bot, instigator, "When using set, you must specify a value. " + incorrectdisplay)
                return
            if target == 'everyone':
                targets = []
                for u in botvisibleusers:
                    targets.append(u)
            else:
                targets = [target]
                #set_database_value(bot, duelrecorduser, 'chanstatsreset', now)
                #reset_database_value(bot, duelrecorduser, 'tier')
                #reset_database_value(bot, duelrecorduser, 'specevent')
                #for u in botvisibleusers:
                #    if statset == 'all':
                #         for x in duelstatsadminarray:
                #             set_database_value(bot, u, x, newvalue)
                #    else:
                #        set_database_value(bot, u, statset, newvalue)
                #osd_notice(bot, instigator, "Possibly done Adjusting stat(s).")
            for player in targets:
                try:
                    if newvalue.isdigit():
                        newvalue = int(newvalue)
                except AttributeError:
                    newvalue = newvalue
                if statset == 'all':
                    for x in duelstatsadminarray:
                        set_database_value(bot, player, x, newvalue)
                else:
                    set_database_value(bot, player, statset, newvalue)
            osd_notice(bot, instigator, "Possibly done Adjusting stat(s).")
    elif subcommand == 'channel':
        settingchange = get_trigger_arg(bot, triggerargsarray, 3)
        if not settingchange:
            osd_notice(bot, instigator, "What channel setting do you want to change?")
        elif settingchange == 'statreset':
            set_database_value(bot, duelrecorduser, 'chanstatsreset', now)
        elif settingchange == 'lastassault':
            reset_database_value(bot, duelrecorduser, 'lastfullroomassultinstigator')
            osd_notice(bot, instigator, "Last Assault Instigator removed.")
            reset_database_value(bot, duelrecorduser, 'lastfullroomassult')
        elif settingchange == 'lastroman':
            reset_database_value(bot, duelrecorduser, 'lastfullroomcolosseuminstigator')
            osd_notice(bot, instigator, "Last Colosseum Instigator removed.")
            reset_database_value(bot, duelrecorduser, 'lastfullroomcolosseum')
        elif settingchange == 'lastinstigator':
            reset_database_value(bot, duelrecorduser, 'lastinstigator')
            osd_notice(bot, instigator, "Last Fought Instigator removed.")
        elif settingchange == 'halfhoursim':
            osd_notice(bot, instigator, "Simulating the half hour automated events.")
            halfhourtimer(bot)
        else:
            osd_notice(bot, instigator, "Must be an invalid command.")
    elif subcommand == 'deathblow':
        newsetting = get_trigger_arg(bot, triggerargsarray, 3).lower()
        set_database_value(bot, instigator, 'deathblowtarget', newsetting)
        set_database_value(bot, instigator, 'deathblowtargettime', now)
    else:
        osd_notice(bot, instigator, "An admin command has not been written for the " + subcommand + " command.")

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

                uClass = get_database_value(bot, u, 'Class') or 'notClassy'
                mana = get_database_value(bot, u, 'mana') or 0

                ## Random user gets a mysterypotion
                lasttimedlootwinner = get_database_value(bot, duelrecorduser, 'lasttimedlootwinner') or bot.nick
                if u != lasttimedlootwinner:
                    randomuarray.append(u)

                ## award coin to all
                adjust_database_value(bot, u, 'coin', halfhour_coin)

                ## health regenerates for all
                set_database_value(bot, u, 'stamina', staminamax)
                for part in stats_healthbodyparts:
                    currenthealthtier = tierratio_level(bot)
                    maxhealthpart = array_compare(bot, part, stats_healthbodyparts, health_bodypart_max)
                    maxhealthpart = int(maxhealthpart)
                    currenthealthtier = currenthealthtier * int(maxhealthpart)
                    currenthealthtier = int(currenthealthtier)
                    currenthealthsplit = maxhealthpart / 2
                    healthsplit = halfhour_regen_health / len(stats_healthbodyparts)
                    gethowmany = get_database_value(bot, u, part) or 0
                    if not gethowmany or gethowmany <= 0 or gethowmany > currenthealthtier:
                        set_database_value(bot, u, part, currenthealthtier)
                    elif gethowmany < currenthealthsplit:
                        adjust_database_value(bot, u, part, healthsplit)
                        gethowmany = get_database_value(bot, u, part) or 0
                        if gethowmany > currenthealthsplit:
                            set_database_value(bot, u, part, currenthealthsplit)

                ## mages regen mana
                if uClass == 'mage':
                    if int(mana) < magemanaregencurrent:
                        adjust_database_value(bot, u, 'mana', halfhour_regen_mage_mana)
                        mana = get_database_value(bot, u, 'mana')
                        if int(mana) > magemanaregencurrent:
                            set_database_value(bot, u, 'mana', magemanaregencurrent)

    ## Log Out Users
    duels_enabled_channels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
    if logoutarray != []:
        dispmsgarray = []
        logoutusers = get_trigger_arg(bot, logoutarray, 'list')
        if len(logoutarray) > 1:
            dispmsgarray.append(logoutusers + " have been logged out of duels for inactivity!")
        else:
            dispmsgarray.append(logoutusers + " has been logged out of duels for inactivity!")
        onscreentext(bot, duels_enabled_channels, dispmsgarray)
        adjust_database_array(bot, duelrecorduser, logoutarray, 'duelusers', 'del')

    ## Random winner select
    if randomuarray != []:
        lootwinner = halfhourpotionwinner(bot, randomuarray)
        adjust_database_value(bot, lootwinner, 'mysterypotion', 1)
        osd_notice(bot, lootwinner, "You have been awarded a mysterypotion! Use .duel loot use mysterypotion to consume.")

## Select winner of potion
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
    lootwinner = get_trigger_arg(bot, winnerselectarray, 'random') or bot.nick
    adjust_database_array(bot, duelrecorduser, [lootwinner], 'lasttimedlootwinners', 'add')
    set_database_value(bot, duelrecorduser, 'lasttimedlootwinner', lootwinner)
    return lootwinner

##########################
## New Checks and setup ##
##########################

def use_loot_item(bot, nickusing, target, targetClass, targetrace, lootitem, quantity, extramsg, lootusedeaths):

    ## Healthpotion
    if lootitem == 'healthpotion':
        if targetrace == 'barbarian':
            potionmaths = int(quantity) * healthpotion_worth_barbarian
        else:
            potionmaths = int(quantity) * healthpotion_worth
        extramsg.append("Restoration of " + str(potionmaths) + " health.")
        splitdamage = potionmaths / len(stats_healthbodyparts)
        for part in stats_healthbodyparts:
            adjust_database_value(bot, target, part, splitdamage)

    ## Poison Potion
    elif lootitem == 'poisonpotion':
        poisonpotionworthb = abs(poisonpotion_worth)
        potionmaths = int(quantity) * int(poisonpotionworthb)
        extramsg.append("Draining of " + str(potionmaths) + " health.")
        splitdamage = poisonpotion_worth / len(stats_healthbodyparts)
        for part in stats_healthbodyparts:
            adjust_database_value(bot, target, part, splitdamage)

    ## Manapotion
    elif lootitem == 'manapotion':
        if targetClass == 'mage':
            potionmaths = int(quantity) * manapotion_worth_mage
        else:
            potionmaths = int(quantity) * manapotion_worth
        extramsg.append("Restoration of " + str(potionmaths) + " mana.")
        adjust_database_value(bot, target, 'mana', potionmaths)

    ## Staminapotion
    elif lootitem == 'staminapotion':
        potionmaths = int(quantity) * staminapotion_worth
        extramsg.append("Restoration of " + str(potionmaths) + " stamina.")
        adjust_database_value(bot, target, 'stamina', potionmaths)

    ## Timepotion
    elif lootitem == 'timepotion':
        extramsg.append("Removal of Timeouts.")
        reset_database_value(bot, target, 'lastfought')
        if duel_combat_timeouts == 'true':
            reset_database_value(bot, duelrecorduser, 'timeout_timeout')
        for k in timepotiontargetarray:
            targetequalcheck = get_database_value(bot, bot.nick, k) or bot.nick
            if targetequalcheck == target:
                reset_database_value(bot, bot.nick, k)
        for j in timepotiontimeoutarray:
            reset_database_value(bot, target, j)
        if duel_combat_timeouts == 'true':
            reset_database_value(bot, bot.nick, 'timeout_timeout')

    ## Check if this action killed the target
    targetheadhealth = get_database_value(bot, target, 'head')
    targettorsohealth = get_database_value(bot, target, 'torso')
    if targetheadhealth  <= 0 or targettorsohealth <= 0:
        if target == instigator:
            deathmsgb = suicidekill(bot,loser) or []
        else:
            deathmsgb = whokilledwhom(bot, instigator, target) or []
        lootusedeaths = lootusedeaths + 1
        for message in deathmsgb:
            extramsg.append(message)

    return extramsg, lootusedeaths

def find_switch_equal(bot, inputarray, switch):
    exitoutput = ''
    switchtofind = str("-"+str(switch)+'="')
    arraymarker = 0
    beguinemark,finishmark = 0,0
    if [wordpart for wordpart in inputarray if wordpart.startswith(switchtofind)]:
        for partial in inputarray:
            arraymarker = arraymarker + 1
            if partial.startswith(switchtofind):
                beguinemark = arraymarker
            if partial.endswith('"'):
                if not finishmark and beguinemark != 0:
                    finishmark = arraymarker
                    continue
        if finishmark != 0:
            exitoutputrange = str(str(beguinemark) + "^" + str(finishmark))
            exitoutput = get_trigger_arg(bot, inputarray, exitoutputrange)
            exitoutput = exitoutput.replace("-"+switch+'=', ' ')
            exitoutput = exitoutput.replace('"', '')
            exitoutput = exitoutput.strip()
    return exitoutput

def check_game_enabled(bot, trigger, instigator, channel_current, duels_enabled_channels):
    checkpass = 0

    ## No Channels Enabled
    if duels_enabled_channels == []:
        if not trigger.admin:
            osd_notice(bot, instigator, "Duels has not been enabled in any bot channels. Talk to a bot admin.")
            return checkpass

    ## Current Channel is not enabled
    if channel_current not in duels_enabled_channels:
        if not trigger.admin:
            osd_notice(bot, instigator, "Duels has not been enabled in " + channel_current + ". Talk to a bot admin.")
            return checkpass

    checkpass = 1
    return checkpass

def check_instigator(bot, trigger, instigator, commands_valid, dev_bypass_checks, command_main):
    checkpass = 0

    ## Instigator can't be a command, and can't enable duels
    if instigator.lower() in commands_valid:
        osd_notice(bot, instigator, "Your nick is the same as a valid command for duels.")
        return checkpass

    ## Instigator can't duelrecorduser
    if instigator.lower() == duelrecorduser or instigator.lower() in target_ignore_list:
        osd_notice(bot, instigator, "Your nick is not able to play duels.")
        return checkpass

    ## Check if Instigator is Opted in
    dueloptedinarray = get_database_value(bot, duelrecorduser, 'duelusers') or []
    if instigator not in dueloptedinarray:
        instigatoropttime = get_timesince_duels(bot, instigator, 'timeout_opttime')
        if instigatoropttime < timeout_opt and dev_bypass_checks == 1 and not trigger.admin:
            osd_notice(bot, instigator, "You are not opted into duels. It looks like you can't enable/disable duels for " + str(hours_minutes_seconds((timeout_opt - instigatoropttime))) + ".")
            return checkpass
        else:
            if command_main != 'off' and command_main != 'on':
                osd_notice(bot, instigator, "Duels Has been enabled for you automatically. To disable, run .duel off.")
                gameenabledchannels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
                dispmsgarray = []
                dispmsgarray.append(instigator + " has entered the arena!")
                onscreentext(bot, gameenabledchannels, dispmsgarray)
                adjust_database_array(bot, duelrecorduser, [instigator], 'duelusers', 'add')
            checkpass = 1
            return checkpass

    checkpass = 1
    return checkpass

def check_command_full(bot, trigger, instigator, command_full, command_type):
    checkpass = 0

    ## There must be a command passed along with ".duel" and "/me duel"
    if not command_full:
        if command_type != 'actionduel':
            osd_notice(bot, instigator, "You must specify either a target, or a subcommand. Online Docs: " + GITWIKIURL)
        else:
            osd_notice(bot, instigator, "You must specify a target. Online Docs: " + GITWIKIURL)
        return checkpass

    ## Don't attempt multi-commands in /me
    if command_type == 'actionduel':
        if "&&" not in command_full:
            osd_notice(bot, instigator, "you cannot run multiple commands via action.")
            return checkpass

    checkpass = 1
    return checkpass

def users_bot_lists(bot, instigator, commands_valid, channel_current, duel_admin_switch):

    ## user lists
    dueloptedinarray = get_database_value(bot, duelrecorduser, 'duelusers') or []
    botvisibleusers = get_database_value(bot, duelrecorduser, 'botvisibleusers') or []
    currentuserlistarray = []
    botvisibleusersappendarray = []
    for user in bot.users:
        if user not in commands_valid and user.lower() not in target_ignore_list:
            currentuserlistarray.append(user)
            if user not in botvisibleusers:
                botvisibleusersappendarray.append(user)
    adjust_database_array(bot, duelrecorduser, botvisibleusersappendarray, 'botvisibleusers', 'add')
    botvisibleusers = get_database_value(bot, duelrecorduser, 'botvisibleusers') or []

    ## Current Duelable Players
    currentduelplayersarray = []
    canduelarray = []
    dowedisplay = 0
    charactercreated = get_database_value(bot, duelrecorduser, 'charactercreatedb') or []
    for player in currentuserlistarray:
        if player in dueloptedinarray and player in charactercreated:
            currentduelplayersarray.append(player)
    for player in currentduelplayersarray:
        executedueling = duelcriteriashort(bot, instigator, player, currentduelplayersarray, channel_current, duel_admin_switch)
        if executedueling == 1:
            canduelarray.append(player)
    random.shuffle(canduelarray)

    return botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray

def alternative_commands_valid(bot):
    altcoms = []
    for subcom in duels_commands_alternate_list:
        duels_commands_alternate_eval = eval("duels_commands_alternate_"+subcom)
        for x in duels_commands_alternate_eval:
            altcoms.append(x)
    return altcoms

def valid_bot_channels(bot):
    valid_channel_list = []
    for c in bot.channels:
        valid_channel_list.append(c)
    return valid_channel_list

def check_duels_lockout(bot, instigator):
    checkpass = 0

    duelslockout = get_database_value(bot, duelrecorduser, 'duelslockout') or 0
    if duelslockout:
        lockoutsince = get_timesince_duels(bot, instigator, 'duelslockout')
        if lockoutsince < duel_lockout_timer:
            osd_notice(bot, instigator, "Duel(s) is/are currently in progress. You must wait. If this is an error, it should clear itself in 5 minutes.")
            return checkpass
        reset_database_value(bot, duelrecorduser, 'duelslockout')

    checkpass = 1
    return checkpass

def command_spelling_check(bot, trigger, triggerargsarray, instigator, now, duels_dev_channels, commands_valid, command_full, command_main, channel_current, command_type, botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray, altcoms, duels_enabled_channels, duel_admin_switch):
    comorig = command_main

    ## Check Commands
    for com in commands_valid:
        similarlevel = similar(command_main.lower(),com)
        if similarlevel >= .75:
            command_main = com
            command_main_process(bot, trigger, triggerargsarray, instigator, now, duels_dev_channels, commands_valid, command_full, command_main, channel_current, command_type, botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray, duels_enabled_channels, duel_admin_switch)
            return

    ## Check alt commands
    if command_main == comorig:
        for com in altcoms:
            similarlevel = similar(command_main.lower(),com)
            if similarlevel >= .75:
                command_main = com
                command_main_process(bot, trigger, triggerargsarray, instigator, now, duels_dev_channels, commands_valid, command_full, command_main, channel_current, command_type, botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray, duels_enabled_channels, duel_admin_switch)
                return

    ## Check players, but only if we didn't alreayd match a command
    if command_main == comorig:
        for player in botvisibleusers:
            similarlevel = similar(command_main.lower(),player)
            if similarlevel >= .75:
                command_main = player
                command_main_process(bot, trigger, triggerargsarray, instigator, now, duels_dev_channels, commands_valid, command_full, command_main, channel_current, command_type, botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray, duels_enabled_channels, duel_admin_switch)
                return

    ## Did we match?
    if command_main != comorig:
        command_main_process(bot, trigger, triggerargsarray, instigator, now, duels_dev_channels, commands_valid, command_full, command_main, channel_current, command_type, botvisibleusers, currentuserlistarray, dueloptedinarray, currentduelplayersarray, canduelarray, duels_enabled_channels, duel_admin_switch)
    else:
        validtarget, validtargetmsg = targetcheck(bot, command_main, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch)
        if not validtarget:
            onscreentext(bot, [instigator], validtargetmsg)
    return

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

def duels_valid_commands(bot):
    duelcommandsarray = []
    for i in range(0,16):
        tiercheck = eval("duels_commands_tier_unlocks_"+str(i))
        for x in tiercheck:
            duelcommandsarray.append(x)
    return duelcommandsarray

###########
## Tiers ##
###########

def tier_command(bot, command):
    tiercommandeval = 0
    for i in range(0,16):
        tiercheck = eval("duels_commands_tier_unlocks_"+str(i))
        if command.lower() in tiercheck:
            tiercommandeval = int(i)
            continue
    return tiercommandeval

def tier_pepper(bot, pepper):
    tiernumber = duels_tier.pepper.index(pepper.lower())
    return tiernumber

def pepper_tier(bot, tiernumber):
    if not tiernumber:
        pepper = 'n00b'
    else:
        pepper = get_trigger_arg(bot, duels_tier.pepper, tiernumber + 1)
        pepper = pepper.title()
    return pepper

def tier_xp(bot, xp):
    tiernumber = 0
    smallerxparray = []
    for x in duels_tier.xp:
        if x <= xp:
            smallerxparray.append(x)
    if smallerxparray != []:
        bigestxp = max(smallerxparray)
        tiernumber = duels_tier.xp.index(bigestxp)
    return tiernumber

def get_pepper(bot, nick):
    if nick == bot.nick:
        pepper = 'Dragon Breath Chilli'
        return pepper
    xp = get_database_value(bot, nick, 'xp') or 0
    if not xp:
        pepper = 'n00b'
        return pepper
    xptier = tier_xp(bot, xp)
    pepper = pepper_tier(bot, xptier)
    # advance respawn tier
    tiernumber = tier_pepper(bot, pepper)
    currenttier = get_database_value(bot, duelrecorduser, 'tier') or 0
    if tiernumber > currenttier:
        set_database_value(bot, duelrecorduser, 'tier', tiernumber)
    nicktier = get_database_value(bot, nick, 'tier')
    if tiernumber != nicktier:
        set_database_value(bot, nick, 'tier', tiernumber)
    pepper = pepper.title()
    return pepper

def tierratio_level(bot):
    currenttier = get_database_value(bot, duelrecorduser, 'tier') or 1
    tierratio = get_trigger_arg(bot, duels_tier.ratio, currenttier) or 1
    return tierratio

#####################
## Target Criteria ##
#####################

## Target
def targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch):

    ## Guilty until proven Innocent
    validtarget = 1
    validtargetmsg = []

    ## Target is instigator
    if target == instigator:
        return validtarget, validtargetmsg

    ## Null Target
    if not target:
        validtarget = 0
        validtargetmsg.append("You must specify a target.")

    ## Bot
    if target == bot.nick or target.lower() in target_ignore_list:
        validtarget = 0
        validtargetmsg.append(target + " can't be targeted.")

    ## Target can't be a valid command
    if target.lower() in commands_valid:
        validtarget = 0
        validtargetmsg.append(target + "'s nick is the same as a valid command for duels.")

    ## Target can't be duelrecorduser
    if target.lower() == duelrecorduser:
        validtarget = 0
        validtargetmsg.append(target + "'s nick is unusable for duels.")

    ## Offline User
    if target.lower() in [x.lower() for x in botvisibleusers] and target.lower() not in [y.lower() for y in currentuserlistarray]:
        validtarget = 0
        target = actualname(bot, target)
        validtargetmsg.append(target + " is offline right now.")

    ## Opted Out
    if target.lower() in [x.lower() for x in currentuserlistarray] and target.lower() not in [j.lower() for j in dueloptedinarray]:
        target = actualname(bot, target)
        validtarget = 0
        validtargetmsg.append(target + " has duels disabled.")

    charactercreated = get_database_value(bot, duelrecorduser, 'charactercreatedb') or []
    if target not in charactercreated:
        target = actualname(bot, target)
        validtarget = 0
        validtargetmsg.append(target + " has not created their character yet.")

    ## None of the above
    if target.lower() not in [y.lower() for y in currentuserlistarray]:
        target = actualname(bot, target)
        validtarget = 0
        validtargetmsg.append(target + " is either not here, or not a valid nick to target.")

    if target != instigator and validtarget == 1:
        statreset(bot, target)
        healthcheck(bot, target)

    return validtarget, validtargetmsg

## actual nick
def nickcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, commands_valid, duel_admin_switch):

    ## Guilty until proven Innocent
    validtarget = 1
    validtargetmsg = []

    ## Target is instigator
    if target == instigator:
        return validtarget, validtargetmsg

    ## Null Target
    if not target:
        validtarget = 0
        validtargetmsg.append("You must specify a target.")

    ## Bot
    if target == bot.nick or target == 'duelrecorduser':
        validtarget = 0
        validtargetmsg.append(target + " can't be targeted.")

    ## Target can't be a valid command
    if target.lower() in commands_valid:
        validtarget = 0
        validtargetmsg.append(target + "'s nick is the same as a valid command for duels.")

    ## Target can't be duelrecorduser
    if target.lower() == duelrecorduser:
        validtarget = 0
        validtargetmsg.append(target + "'s nick is unusable for duels.")

    ## Offline User
    if target.lower() in [x.lower() for x in botvisibleusers] and target.lower() not in [y.lower() for y in currentuserlistarray]:
        validtarget = 0
        target = actualname(bot, target)
        validtargetmsg.append(target + " is offline right now.")

    charactercreated = get_database_value(bot, duelrecorduser, 'charactercreatedb') or []
    if target not in charactercreated:
        target = actualname(bot, target)
        validtarget = 0
        validtargetmsg.append(target + " has not created their character yet.")

    ## None of the above
    if target.lower() not in [y.lower() for y in currentuserlistarray]:
        target = actualname(bot, target)
        validtarget = 0
        validtargetmsg.append(target + " is either not here, or not a valid nick to target.")

    if target != instigator and validtarget == 1:
        statreset(bot, target)
        healthcheck(bot, target)

    return validtarget, validtargetmsg

# mustpassthesetoduel
def duelcriteria(bot, usera, userb, currentduelplayersarray, channel_current, duel_admin_switch):

    ## Guilty until proven Innocent
    validtarget = 1
    validtargetmsg = []

    ## usera ignores lastfought
    useraClass = get_database_value(bot, usera, 'Class') or 'notClassy'
    if useraClass != 'knight':
        useralastfought = get_database_value(bot, usera, 'lastfought') or ''
    else:
        useralastfought = bot.nick

    ## Timeout Retrieval
    if duel_combat_timeouts == 'true':
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
    howmanyduelusers = len(dueluserslist)

    ## Correct userb Name
    userb = actualname(bot, userb)

    ## Devroom bypass
    duels_dev_channels = get_database_value(bot, duelrecorduser, 'devenabled') or []
    if channel_current in duels_dev_channels or duel_admin_switch:
        validtarget = 1
        return validtarget, validtargetmsg
    if not channel_current.startswith("#") and len(duels_dev_channels) > 0:
        validtarget = 1
        return validtarget, validtargetmsg

    ## Don't allow usera to duel twice in a row
    if usera == channellastinstigator:
        if duel_combat_timeouts == 'true':
            if useratime <= INSTIGATORTIMEOUT:
                validtargetmsg.append("You may not instigate fights twice in a row within a half hour. You must wait for somebody else to instigate., or "+str(hours_minutes_seconds((INSTIGATORTIMEOUT - useratime)))+" .")
        else:
            validtargetmsg.append("You may not instigate fights twice in a row within a half hour. You must wait for somebody else to instigate.")#, or "+str(hours_minutes_seconds((INSTIGATORTIMEOUT - useratime)))+" .")
        validtarget = 0

    ## usera can't duel the same person twice in a row, unless there are only two people in the channel
    if userb == useralastfought and howmanyduelusers > 2:
        validtargetmsg.append('You may not fight the same person twice in a row.')
        validtarget = 0

    charactercreated = get_database_value(bot, duelrecorduser, 'charactercreatedb') or []
    if userb not in charactercreated:
        validtarget = 0
        validtargetmsg.append(userb + " has not created their character yet.")

    ## Timeouts
    if duel_combat_timeouts == 'true':
        ## usera Timeout
        if useratime <= USERTIMEOUT:
            validtargetmsg.append("You can't duel for "+str(hours_minutes_seconds((USERTIMEOUT - useratime)))+".")
            validtarget = 0

        ## Target Timeout
        if userbtime <= USERTIMEOUT:
            validtargetmsg.append(userb + " can't duel for "+str(hours_minutes_seconds((USERTIMEOUT - userbtime)))+".")
            validtarget = 0

        ## Channel Timeout
        if channeltime <= CHANTIMEOUT:
            validtargetmsg.append("Channel can't duel for "+str(hours_minutes_seconds((CHANTIMEOUT - channeltime)))+".")
            validtarget = 0

    return validtarget, validtargetmsg

def duelcriteriashort(bot, usera, userb, currentduelplayersarray, channel_current, duel_admin_switch):

    ## Guilty until proven Innocent
    validtarget = 0

    ## Devroom bypass
    duels_dev_channels = get_database_value(bot, duelrecorduser, 'devenabled') or []
    if channel_current in duels_dev_channels or duel_admin_switch:
        validtarget = 1
        return validtarget
    if not channel_current.startswith("#") and len(duels_dev_channels) > 0:
        validtarget = 1
        return validtarget

    ## Don't allow usera to duel twice in a row
    channellastinstigator = get_database_value(bot, duelrecorduser, 'lastinstigator') or bot.nick
    if duel_combat_timeouts == 'true':
        useratime = get_timesince_duels(bot, usera, 'timeout_timeout') or 0
    if usera == channellastinstigator:
        if duel_combat_timeouts == 'true':
            if useratime <= INSTIGATORTIMEOUT:
                return validtarget
        else:
            return validtarget

    ## usera can't duel the same person twice in a row, unless there are only two people in the channel
    howmanyduelusers = len(currentduelplayersarray)
    if duel_combat_timeouts == 'true':
        userbtime = get_timesince_duels(bot, userb, 'timeout_timeout') or 0
    useralastfought = get_database_value(bot, usera, 'lastfought') or ''
    if userb == useralastfought and howmanyduelusers > 2:
        useraClass = get_database_value(bot, usera, 'Class') or 'notClassy'
        if useraClass != 'knight':
            return validtarget

    charactercreated = get_database_value(bot, duelrecorduser, 'charactercreatedb') or []
    if userb not in charactercreated:
        validtarget = 0

    ## Timeouts
    if duel_combat_timeouts == 'true':
        ## usera Timeout
        if useratime <= USERTIMEOUT:
            return validtarget

        ## Target Timeout
        if userbtime <= USERTIMEOUT:
            return validtarget

        ## Channel Timeout
        channeltime = get_timesince_duels(bot, duelrecorduser, 'timeout_timeout') or 0
        if channeltime <= CHANTIMEOUT:
            return validtarget

    validtarget = 1
    return validtarget

## Events
def eventchecks(bot, canduelarray, command_main, instigator, currentduelplayersarray, channel_current, duel_admin_switch):

    ## Guilty until proven Innocent
    validtarget = 1
    validtargetmsg = []

    if canduelarray == []:
        validtarget = 0
        validtargetmsg.append(instigator + ", It looks like the full channel " + command_main + " event target finder has failed.")
        return validtarget, validtargetmsg

    ## Devroom bypass
    duels_dev_channels = get_database_value(bot, duelrecorduser, 'devenabled') or []
    if channel_current in duels_dev_channels or duel_admin_switch:
        validtarget = 1
        return validtarget, validtargetmsg
    if not channel_current.startswith("#") and len(duels_dev_channels) > 0:
        validtarget = 1
        return validtarget, validtargetmsg

    if instigator not in canduelarray:
        validtarget = 0
        canduel, validtargetmsgb = duelcriteria(bot, instigator, instigator, currentduelplayersarray, channel_current, duel_admin_switch)
        for x in validtargetmsgb:
            validtargetmsg.append(x)

    timeouteval = eval("timeout_"+command_main.lower())
    getlastusage = get_timesince_duels(bot, duelrecorduser, str('lastfullroom' + command_main)) or timeouteval
    getlastinstigator = get_database_value(bot, duelrecorduser, str('lastfullroom' + command_main + 'instigator')) or bot.nick

    if getlastusage < timeouteval:
        validtargetmsg.append("Full channel " + command_main + " event can't be used for "+str(hours_minutes_seconds((timeouteval - getlastusage)))+".")
        validtarget = 0

    if getlastinstigator == instigator:
        validtargetmsg.append("You may not instigate a full channel " + command_main + " event twice in a row.")
        validtarget = 0

    if validtarget == 1:
        for player in canduelarray:
            statreset(bot, player)

    return validtarget, validtargetmsg

############
## Damage ##
############

## bodypart selector
def bodypart_select(bot, nick):
    ## selection roll
    hitchance = randint(1, 101)
    if hitchance <= 50:
        bodypart = 'torso'
    elif hitchance >= 90:
        bodypart = 'head'
    else:
        currentbodypartsarray = bodypartarray(bot, nick)
        bodypart = get_trigger_arg(bot, currentbodypartsarray, 'random')
    if "_" in bodypart:
        bodypartname = bodypart.replace("_", " ")
    else:
        bodypartname = bodypart
    return bodypart, bodypartname

## Damage Caused
def duels_damage(bot, damagescale, Classwinner, racewinner, Classloser, winner, loser):

    ## Rogue can't be hurt by themselves or bot
    if Classloser == 'rogue' and winner == loser:
        damage = 0

    ## Bot deals a set amount
    elif winner == bot.nick:
        if Classloser == 'rogue':
            damage = 0
        else:
            damage = bot_damage

    ## Barbarians get extra damage (minimum)
    elif racewinner == 'barbarian':
        damage = randint(duel_advantage_barbarian_min_damage, 120)

    ## vampires have a minimum damage
    elif racewinner == 'vampire' and winner != loser:
        damage = randint(0, duel_disadvantage_vampire_max_damage)

    ## All Other Players
    else:
        damage = randint(0, 120)

    ## Damage Tiers
    if damage > 0:
        damage = damagescale * damage
        damage = int(damage)

    return damage

## Damage Text
def duels_damage_text(bot, damage, winnername, losername, bodypart, striketype, weapon, Classwinner, racewinner, bodypartname):

    if losername == winnername:
        losername = "themself"
    if damage == 0:
        damagetext = str(winnername + " " + striketype + " " + losername + " in the " + bodypartname + weapon + ', but deals no damage.')
    elif racewinner == 'vampire' and winnername != losername:
        damagetext = str(winnername + " drains " + str(damage)+ " health from " + losername + weapon + " in the " + bodypartname + ".")
    else:
        damagetext = str(winnername + " " + striketype + " " + losername + " in the " + bodypartname + weapon + ", dealing " + str(damage) + " damage.")
    return damagetext

## Damage Resistance
def damage_resistance(bot, nick, damage, bodypart):
    damagetextarray = []

    ## Shields
    if damage > 0:
        shieldnick = get_database_value(bot, nick, 'shield') or 0
        if shieldnick:
            damagemath = int(shieldnick) - damage
            if int(damagemath) > 0:
                adjust_database_value(bot, nick, 'shield', -abs(damage))
                damage = 0
                absorbed = 'all'
            else:
                absorbed = damagemath + damage
                damage = abs(damagemath)
                reset_database_value(bot, nick, 'shield')
            damagetextarray.append(nick + " absorbs " + str(absorbed) + " of the damage. ")

    ## Armor
    if damage > 0:
        armortype = array_compare(bot, bodypart, stats_healthbodyparts, stats_armor)
        armornick = get_database_value(bot, nick, armortype) or 0
        if armornick:
            armorname = armortype.replace("_", " ")
            adjust_database_value(bot, nick, armortype, -1)
            damagepercent = randint(1, armor_relief_percentage) / 100
            damagereduced = damage * damagepercent
            damagereduced = int(damagereduced)
            damage = damage - damagereduced
            if nick.endswith('s'):
                damagenick = str(nick + "'")
            else:
                damagenick = str(nick + "s")
            damagetext = str(damagenick + " "+ armorname + " alleviated " + str(damagereduced) + " of the damage.")
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

## player killed a player
def whokilledwhom(bot, winner, loser):
    winnertextarray = []
    winnertextarray.append(loser + ' dies forcing a respawn!!')
    ## Reset mana and health
    reset_database_value(bot, loser, 'mana')
    healthfresh(bot, loser) ## TODO, replace with just building the health
    ## update kills/deaths
    adjust_database_value(bot, winner, 'kills', 1)
    adjust_database_value(bot, loser, 'respawns', 1)
    ## Loot Corpse
    loserClass = get_database_value(bot, loser, 'Class') or 'notClassy'
    bountyonloser = get_database_value(bot, loser, 'bounty')
    if bountyonloser:
        adjust_database_value(bot, winner, 'coin', bountyonloser)
        reset_database_value(bot, loser, 'bounty')
        winnertextarray.append(winner + " wins a bounty of " + str(bountyonloser) + " that was placed on " + loser + ".")
    ## stamina at max
    set_database_value(bot, loser, 'stamina', staminamax)
    ## rangers don't lose their stuff
    if loserClass != 'ranger':
        for x in loot_all_types:
            gethowmany = get_database_value(bot, loser, x)
            ## TODO array of loot won
            adjust_database_value(bot, winner, x, gethowmany)
            reset_database_value(bot, loser, x)
    return winnertextarray

## player killed themself
def suicidekill(bot,loser):
    suicidetextarray = []
    suicidetextarray.append(loser + " committed suicide, forcing a respawn.")
    ## Reset mana
    reset_database_value(bot, loser, 'mana')
    suicidetextarray.append(loser + " lose all mana.")
    ## Stock health
    #set_database_value(bot, loser, 'health_b4se', stockhealth)
    healthfresh(bot, loser) ## TODO: non-tiered
    ## update deaths
    adjust_database_value(bot, loser, 'respawns', 1)
    ## bounty
    bountyonloser = get_database_value(bot, loser, 'bounty')
    if bountyonloser:
        suicidetextarray.append(loser + " wastes the bounty of " + str(bountyonloser) + " coin.")
    reset_database_value(bot, loser, 'bounty')
    ## stamina at 0
    set_database_value(bot, loser, 'stamina', 2)
    ## rangers don't lose their stuff
    loserClass = get_database_value(bot, loser, 'Class') or 'notClassy'
    if loserClass != 'ranger':
        for x in loot_all_types:
            reset_database_value(bot, loser, x)
        suicidetextarray.append(loser + " loses all loot.")
    return suicidetextarray

## Verify health is not below zero, and not above max
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
    mana = get_database_value(bot, nick, 'mana')
    if int(mana) <= 0:
        reset_database_value(bot, nick, 'mana')
    ## stamina at max
    stamina = get_database_value(bot, nick, 'stamina')
    if int(stamina) <= 0 or int(stamina) > staminamax:
        set_database_value(bot, nick, 'stamina', staminamax)

## Health after death
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
    mana = get_database_value(bot, nick, 'mana')
    if int(mana) <= 0:
        reset_database_value(bot, nick, 'mana')
    ## stamina at max
    stamina = get_database_value(bot, nick, 'stamina')
    if int(stamina) <= 0 or int(stamina) > staminamax:
        set_database_value(bot, nick, 'stamina', staminamax)

## Total Health
def get_health(bot,nick):
    totalhealth = 0
    for x in stats_healthbodyparts:
        gethowmany = get_database_value(bot, nick, x)
        if gethowmany:
            totalhealth = totalhealth + gethowmany
    return totalhealth

## Non-Crippled Body Parts
def bodypartarray(bot, nick):
    currentbodypartsarray = []
    for x in stats_healthbodyparts:
        gethowmany = get_database_value(bot, nick, x)
        if gethowmany:
            currentbodypartsarray.append(x)
    return currentbodypartsarray

def deathblowcheck(bot, instigator):
    deathblowtarget = get_database_value(bot, instigator, 'deathblowtarget')
    if deathblowtarget:
        deathblowtargettime = get_timesince_duels(bot, instigator, 'deathblowtargettime') or 0
        if deathblowtargettime > 30:
            reset_database_value(bot, instigator, 'deathblowtarget')
            reset_database_value(bot, instigator, 'deathblowtargettime')
        else:
            nickhealth = get_health(bot,deathblowtarget)
            if nickhealth > 100:
                 reset_database_value(bot, instigator, 'deathblowtarget')
                 reset_database_value(bot, instigator, 'deathblowtargettime')

################
## User Nicks ##
################

## Build Duel Name Text
def duel_names(bot, nick, channel):
    if nick == 'duelsmonster':
        nickname = get_trigger_arg(bot, monstersarray, 'random')
        nickname = str("A lower level "+nickname)
        return nickname
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

## Titles
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

## Pepper
def nickpepper(bot, nick, channel):
    pepperstart = get_pepper(bot, nick)
    if not pepperstart or pepperstart == '':
        nickname = "(n00b)"
    else:
        nickname = str("(" + pepperstart.title() + ")")
    return nickname

## Magic
def nickmagicattributes(bot, nick, channel):
    nickname = ''
    nickcurse = get_database_value(bot, nick, 'curse')
    nickshield = get_database_value(bot, nick, 'shield')
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

## Armored
def nickarmor(bot, nick, channel):
    nickname = ''
    for x in stats_armor:
        gethowmany = get_database_value(bot, nick, x)
        if gethowmany:
            nickname = "{Armored}"
    return nickname

## Outputs Nicks with correct capitalization
def actualname(bot,nick):
    actualnick = nick
    for u in bot.users:
        if u.lower() == nick.lower():
            actualnick = u
    return actualnick

##########
## Time ##
##########

## compare timestamps
def get_timesince_duels(bot, nick, databasekey):
    now = time.time()
    last = get_database_value(bot, nick, databasekey)
    return abs(now - int(last))

## Get timediff for user timeouts for stats display
def get_timeout_timeout(bot, nick):
    if duel_combat_timeouts == 'true':
        timediff = 0
        return timediff
    time_since = get_timesince_duels(bot, nick, 'timeout_timeout')
    if time_since < USERTIMEOUT:
        timediff = str(hours_minutes_seconds((USERTIMEOUT - time_since)))
    else:
        timediff = 0
    return timediff

## Convert seconds to a readable format
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

## Chance of Finding loot in a duel
def randominventory(bot, instigator):
    yourClass = get_database_value(bot, instigator, 'Class') or 'notClassy'
    if yourClass == 'scavenger':
        randomfindchance = randint(duel_advantage_scavenger_loot_find, 100)
    else:
        randomfindchance = randint(0, 120)
    randominventoryfind = 'false'
    if randomfindchance >= 90:
        randominventoryfind = 'true'
    return randominventoryfind

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
    weapon = get_trigger_arg(bot, allchanweaponsarray, 'random')
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
    weapon = get_trigger_arg(bot, weaponslistselect, 'random') or 'fist'
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
    elif weapon.lower().startswith(' with'):
        weapon = str(weapon).strip()
    else:
        weapon = str('with a ' + weapon)
    return weapon

################
## Stat Reset ##
################

def chanstatreset(bot):
    now = time.time()
    duelstatsadminarray = duels_valid_stats(bot)
    for x in duelstatsadminarray:
        reset_database_value(bot, duelrecorduser, "usage_"+x)
        reset_database_value(bot, bot.nick, "usage_"+x)
        reset_database_value(bot, duelrecorduser, "usage_total")
        reset_database_value(bot, bot.nick, "usage_total")
        reset_database_value(bot, bot.nick, x)
        reset_database_value(bot, duelrecorduser, x)
    set_database_value(bot, duelrecorduser, 'chanstatsreset', now)

def duelrecordwipe(bot):
    chanrecordsarray = ['gameenabled','devenabled','botvisibleusers','duelusers','duelslockout','tier','lastinstigator','timeout_timeout','specevent','roulettelastplayershot','roulettelastplayer','roulettecount','roulettechamber','roulettespinarray','roulettewinners','lasttimedlootwinner']
    eventsarray = ['roulette','colosseum','assault']
    for event in eventsarray:
        reset_database_value(bot, duelrecorduser, "lastfullroom" + event)
        reset_database_value(bot, bot.nick, "lastfullroom" + event)
    for astat in assault_results:
        reset_database_value(bot, duelrecorduser, "assault_" + astat)
        reset_database_value(bot, bot.nick, "assault_" + astat)
    for record in chanrecordsarray:
        reset_database_value(bot, duelrecorduser, record)
        reset_database_value(bot, bot.nick, record)

def statreset(bot, nick):
    now = time.time()
    getlastchanstatreset = get_database_value(bot, duelrecorduser, 'chanstatsreset')
    if not getlastchanstatreset:
        set_database_value(bot, duelrecorduser, 'chanstatsreset', now)
    getnicklastreset = get_database_value(bot, nick, 'chanstatsreset')
    if getnicklastreset < getlastchanstatreset:
        duelstatsadminarray = duels_valid_stats(bot)
        for x in duelstatsadminarray:
            reset_database_value(bot, nick, "usage_"+x)
            reset_database_value(bot, nick, x)
        set_database_value(bot, nick, 'chanstatsreset', now)
        reset_database_value(bot, nick, "usage_combat")
        reset_database_value(bot, nick, "usage_total")
        reset_database_value(bot, nick, "roulettepayout")

## Bot no stats
def refreshbot(bot):
    duelstatsadminarray = duels_valid_stats(bot)
    for x in duelstatsadminarray:
        set_database_value(bot, bot.nick, x, None)

def refreshduelsmonster(bot):
    duelstatsadminarray = duels_valid_stats(bot)
    for x in duelstatsadminarray:
        set_database_value(bot, 'duelsmonster', x, None)

def monsterstats(bot, currentduelplayersarray, scale):
    duelstatsadminarray = duels_valid_stats(bot)
    for x in duelstatsadminarray:
        playerstatarrayaverage = 0
        currentstatarray = []
        for player in currentduelplayersarray:
            playernumber = get_database_value(bot, player, x)
            if str(playernumber).isdigit():
                currentstatarray.append(playernumber)
        if playerstatarrayaverage == []:
            playerstatarrayaverage = mean(currentstatarray)
            playerstatarrayaverage = int(playerstatarrayaverage)
        else:
            playerstatarrayaverage = 0
        if playerstatarrayaverage > 0:
            set_database_value(bot, 'duelsmonster', x, int(playerstatarrayaverage * scale))

######################
## Winner Selection ##
######################

## Select winner from an array (stat based)
def selectwinner(bot, nickarray):
    statcheckarray = ['health','xp','kills','respawns','streak_win_current']

    ## empty var to start
    for user in nickarray:
        reset_database_value(bot, user, 'winnerselection')

    ## everyone gets a roll
    for user in nickarray:
        adjust_database_value(bot, user, 'winnerselection', 1)

    ## random roll
    randomrollwinner = get_trigger_arg(bot, nickarray, 'random')
    adjust_database_value(bot, randomrollwinner, 'winnerselection', 1)

    ## Stats
    playerarray,statvaluearray = [],[]
    for x in statcheckarray:
        for u in nickarray:
            if x != 'health':
                value = get_database_value(bot, u, x) or 0
            else:
                scriptdef = str('get_' + x + '(bot,u)')
                value = eval(scriptdef)
            playerarray.append(u)
            statvaluearray.append(x)
        statvaluearray, playerarray = array_arrangesort(bot, statvaluearray, playerarray)
        if x == 'respawns' or x == 'streak_win_current':
            statleadername = get_trigger_arg(bot, playerarray, 1)
            statleadernumber = get_trigger_arg(bot, statvaluearray, 1)
        else:
            statleadername = get_trigger_arg(bot, playerarray, 'last')
            statleadernumber = get_trigger_arg(bot, statvaluearray, 'last')
        adjust_database_value(bot, statleadername, 'winnerselection', 1)

    ## weaponslocker not empty
    for user in nickarray:
        weaponslist = get_database_value(bot, user, 'weaponslocker_complete') or []
        if weaponslist != []:
            adjust_database_value(bot, user, 'winnerselection', 1)

    ## anybody rogue?
    for user in nickarray:
        nickClass = get_database_value(bot, user, 'Class') or ''
        if nickClass == 'rogue':
            adjust_database_value(bot, user, 'winnerselection', 1)

    ## Dice rolling occurs now
    for user in nickarray:
        rolls = get_database_value(bot, user, 'winnerselection') or 0
        maxroll = winnerdicerolling(bot, user, rolls)
        set_database_value(bot, user, 'winnerselection', maxroll)

    ## curse check
    for user in nickarray:
        cursed = get_database_value(bot, user, 'curse') or 0
        if cursed:
            reset_database_value(bot, user, 'winnerselection')
            adjust_database_value(bot, user, 'curse', -1)

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

## Max diceroll
def winnerdicerolling(bot, nick, rolls):
    nickClass = get_database_value(bot, nick, 'Class') or ''
    rolla = 0
    rollb = 20
    if nickClass == 'rogue':
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
    nickshield = get_database_value(bot, nick, 'shield') or 0
    nickcurse = get_database_value(bot, nick, 'curse') or 0
    return nickshield, nickcurse

def get_magic_attributes_text(bot, winner, loser, winnershieldstart, losershieldstart, winnercursestart, losercursestart):
    attributetext = []
    winnershieldnow, winnercursenow = get_current_magic_attributes(bot, winner)
    losershieldnow, losercursenow = get_current_magic_attributes(bot, loser)
    magicattributesarray = ['shield','curse']
    nickarray = ['winner','loser']
    attributetext = []
    for j in nickarray:
        person = eval(j)
        for x in magicattributesarray:
            workingvarnow = eval(j+x+"now")
            workingvarstart = eval(j+x+"start")
            if workingvarnow == 0 and workingvarnow != workingvarstart:
                attributetext.append(person + " is no longer affected by " + str(x) + ".")
    return attributetext

###############
## ScoreCard ##
###############

## compare wins/losses
def get_winlossratio(bot,target):
    wins = get_database_value(bot, target, 'wins')
    wins = int(wins)
    losses = get_database_value(bot, target, 'losses')
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

#############
## Stamina ##
#############

def staminacheck(bot, nick, channel_current, command, duel_admin_switch):

    ## Devroom bypass
    duels_dev_channels = get_database_value(bot, duelrecorduser, 'devenabled') or []
    if channel_current in duels_dev_channels or duel_admin_switch:
        staminapass = 1
        return staminapass
    if not channel_current.startswith("#") and len(duels_dev_channels) > 0:
        staminapass = 1
        return staminapass


    stamina = get_database_value(bot, nick, 'stamina') or 0
    if command in duels_commands_stamina_free:
        commandstaminacost = 0
    else:
        commandstaminacost = eval("duels_commands_stamina_"+command)
    staminapass = 0
    if commandstaminacost <= stamina:
        staminapass = 1
    return staminapass

def staminacharge(bot, nick, command):
    if command in duels_commands_stamina_free:
        commandstaminacost = 0
    else:
        commandstaminacost = eval("duels_commands_stamina_"+command)
        adjust_database_value(bot, nick, 'stamina', -abs(commandstaminacost))

#############
## Similar ##
#############

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

###################
## Duels Version ##
###################

def versionnumber(bot):
    duels_version_plainnow = duels_version_plain
    page = requests.get(duels_version_github_page,headers = None)
    if page.status_code == 200:
        tree = gettree()
        duels_version_plainnow = str(tree.xpath(duels_version_github_xpath))
        for r in (("\\n", ""), ("['",""), ("']",""), ("'",""), ('"',""), (',',""), ('Commits on',"")):
            duels_version_plainnow = duels_version_plainnow.replace(*r)
        duels_version_plainnow = duels_version_plainnow.strip()
    return duels_version_plainnow

def gettree():
    page = requests.get(duels_version_github_page,headers = None)
    tree= html.fromstring(page.content)
    return tree

##############
## Database ##
##############

## Get a value
def get_database_value(bot, nick, databasekey):
    databasecolumn = str('duels_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

## set a value
def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('duels_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)

## set a value to None
def reset_database_value(bot, nick, databasekey):
    databasecolumn = str('duels_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, None)

## add or subtract from current value
def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey) or 0
    databasecolumn = str('duels_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))

## array stored in database length
def get_database_array_total(bot, nick, databasekey):
    array = get_database_value(bot, nick, databasekey) or []
    entriestotal = len(array)
    return entriestotal

## array stored in database, add or remove elements
def adjust_database_array(bot, nick, entries, databasekey, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
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

######################
## On Screen Text ##
######################

def osd_notice(bot, target, textarraycomplete):
    target = actualname(bot,target)
    if not isinstance(textarraycomplete, list):
        texttoadd = str(textarraycomplete)
        textarraycomplete = []
        textarraycomplete.append(texttoadd)
    passthrough = []
    passthrough.append(target + ", ")
    for x in textarraycomplete:
        passthrough.append(x)
    onscreentext(bot, [target], passthrough)

def onscreentext(bot, texttargetarray, textarraycomplete):
    if not isinstance(textarraycomplete, list):
        texttoadd = str(textarraycomplete)
        textarraycomplete = []
        textarraycomplete.append(texttoadd)
    if not isinstance(texttargetarray, list):
        target = texttargetarray
        texttargetarray = []
        texttargetarray.append(target)
    combinedtextarray = []
    currentstring = ''
    for textstring in textarraycomplete:
        if currentstring == '':
            currentstring = textstring
        elif len(textstring) > 200:
            if currentstring != '':
                combinedtextarray.append(currentstring)
                currentstring = ''
            combinedtextarray.append(textstring)
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

####################################
## Array/List/String Manipulation ##
####################################

## Hub
def get_trigger_arg(bot, inputs, outputtask):
    ## Create
    if outputtask == 'create':
        return create_array(bot, inputs)
    ## reverse
    if outputtask == 'reverse':
        return reverse_array(bot, inputs)
    ## Comma Seperated List
    if outputtask == 'list':
        return list_array(bot, inputs)
    if outputtask == 'random':
        return random_array(bot, inputs)
    ## Last element
    if outputtask == 'last':
        return last_array(bot, inputs)
    ## Complete String
    if outputtask == 0 or outputtask == 'complete' or outputtask == 'string':
        return string_array(bot, inputs)
    ## Number
    if str(outputtask).isdigit():
        return number_array(bot, inputs, outputtask)
    ## Exlude from array
    if str(outputtask).endswith("!"):
        return excludefrom_array(bot, inputs, outputtask)
    ## Inclusive range starting at
    if str(outputtask).endswith("+"):
        return incrange_plus_array(bot, inputs, outputtask)
    ## Inclusive range ending at
    if str(outputtask).endswith("-"):
        return incrange_minus_array(bot, inputs, outputtask)
    ## Exclusive range starting at
    if str(outputtask).endswith(">"):
        return excrange_plus_array(bot, inputs, outputtask)
    ## Exclusive range ending at
    if str(outputtask).endswith("<"):
        return excrange_minus_array(bot, inputs, outputtask)
    ## Range Between Numbers
    if "^" in str(outputtask):
        return rangebetween_array(bot, inputs, outputtask)
    string = ''
    return string

## Convert String to array
def create_array(bot, inputs):
    if isinstance(inputs, list):
        string = ''
        for x in inputs:
            if string != '':
                string = str(string + " " + str(x))
            else:
                string = str(x)
        inputs = string
    outputs = []
    if inputs:
        for word in inputs.split():
            outputs.append(word)
    return outputs

## Convert Array to String
def string_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    for x in inputs:
        if string != '':
            string = str(string + " " + str(x))
        else:
            string = str(x)
    return string

## output reverse order
def reverse_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    if len(inputs) == 1:
        return inputs
    outputs = []
    if inputs == []:
        return outputs
    for d in inputs:
        outputs.append(d)
    outputs.reverse()
    return outputs

## Comma Seperated List
def list_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    for x in inputs:
        if string != '':
            string  = str(string  + ", " + x)
        else:
            string  = str(x)
    return string

## Random element
def random_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    temparray = []
    for d in inputs:
        temparray.append(d)
    shuffledarray = random.shuffle(temparray)
    randomselected = random.randint(0,len(temparray) - 1)
    string = str(temparray [randomselected])
    return string

## Last element
def last_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    string = inputs[len(inputs)-1]
    return string

## select a number
def number_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if str(number).isdigit():
        numberadjust = int(number) -1
        if numberadjust< len(inputs) and numberadjust >= 0:
            number = int(number) - 1
            string = inputs[number]
    return string

## range
def range_array(bot, inputs, rangea, rangeb):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    if int(rangeb) == int(rangea):
        return number_array(bot, inputs, rangeb)
    if int(rangeb) < int(rangea):
        tempa, tempb = rangeb, rangea
        rangea, rangeb = tempa, tempb
    if int(rangea) < 1:
        rangea = 1
    if int(rangeb) > len(inputs):
        return string
    for i in range(int(rangea),int(rangeb) + 1):
        arg = number_array(bot, inputs, i)
        if string != '':
            string = str(string + " " + arg)
        else:
            string = str(arg)
    return string

## exclude a number
def excludefrom_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if str(number).endswith("!"):
        number = re.sub(r"!", '', str(number))
    if str(number).isdigit():
        for i in range(1,len(inputs)):
            if int(i) != int(number):
                arg = number_array(bot, inputs, i)
                if string != '':
                    string = str(string + " " + arg)
                else:
                    string = str(arg)
    return string

## range between
def rangebetween_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if "^" in str(number):
        rangea = number.split("^", 1)[0]
        rangeb = number.split("^", 1)[1]
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

## inclusive forward
def incrange_plus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith("+"):
        rangea = re.sub(r"\+", '', str(number))
        rangeb = len(inputs)
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

## inclusive reverse
def incrange_minus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith("-"):
        rangea = 1
        rangeb = re.sub(r"-", '', str(number))
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

## excluding forward
def excrange_plus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith(">"):
        rangea = re.sub(r">", '', str(number))
        rangea = int(rangea) + 1
        rangeb = len(inputs)
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

## excluding reverse
def excrange_minus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith("<"):
        rangea = 1
        rangeb = re.sub(r"<", '', str(number))
        rangeb = int(rangeb) - 1
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

######################
## Array comparison ##
######################

def array_compare(bot, indexitem, arraytoindex, arraytocompare):
    item = ''
    for x, y in zip(arraytoindex, arraytocompare):
        if x == indexitem:
            item = y
    return item

def array_arrangesort(bot, sortbyarray, arrayb):
    sortbyarray, arrayb = (list(x) for x in zip(*sorted(zip(sortbyarray, arrayb),key=itemgetter(0))))
    return sortbyarray, arrayb

