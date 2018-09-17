#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# pylama:ignore=W,E201,E202,E203,E221,E222,w292,E231


"""
Open Dictionary of Users and Locations
"""


rpg_game_dict = {

                # Some values don't get saved to the database, but stay in memory
                "tempvals":{

                            # startupmonologue
                            "startupmonologue": [],
                            "monologuecheck": 1,

                            # Indicate if we need to pull the dict from the database
                            "game_loaded": False,

                            # list of channels the bot is in
                            "channels_list": [],

                            # Other bots
                            "bots_list": [],

                            # current users
                            "current_users": [],

                            # offline users
                            "offline_users": [],

                            # bot owner users
                            "bot_owner": [],

                            # bot admin users
                            "bot_admins": [],

                            # bot owner users
                            "chanops": [],

                            # bot admin users
                            "chanhalfops": [],

                            # bot admin users
                            "chanvoices": [],

                            # End of Temp Vals
                            },

                # Static content
                "static": {
                            #
                            "tier_reference":[

                                                {
                                                    'tier_num': 0,
                                                    'tier_pepper': 'n00b',
                                                    'tier_ratio': 1
                                                },

                                                {
                                                    'tier_num': 1,
                                                    'tier_pepper': 'pimiento',
                                                    'tier_ratio': 1
                                                },

                                                {
                                                    'tier_num': 2,
                                                    'tier_pepper': 'sonora',
                                                    'tier_ratio': 1.1
                                                },

                                                {
                                                    'tier_num': 3,
                                                    'tier_pepper': 'anaheim',
                                                    'tier_ratio': 1.2
                                                },

                                                {
                                                    'tier_num': 4,
                                                    'tier_pepper': 'poblano',
                                                    'tier_ratio': 1.3
                                                },

                                                {
                                                    'tier_num': 5,
                                                    'tier_pepper': 'jalapeno',
                                                    'tier_ratio': 1.4
                                                },

                                                {
                                                    'tier_num': 6,
                                                    'tier_pepper': 'serrano',
                                                    'tier_ratio': 1.5
                                                },

                                                {
                                                    'tier_num': 7,
                                                    'tier_pepper': 'chipotle',
                                                    'tier_ratio': 1.6
                                                },

                                                {
                                                    'tier_num': 8,
                                                    'tier_pepper': 'tabasco',
                                                    'tier_ratio': 1.7
                                                },

                                                {
                                                    'tier_num': 9,
                                                    'tier_pepper': 'cayenne',
                                                    'tier_ratio': 1.8
                                                },

                                                {
                                                    'tier_num': 10,
                                                    'tier_pepper': 'thai pepper',
                                                    'tier_ratio': 1.9
                                                },

                                                {
                                                    'tier_num': 11,
                                                    'tier_pepper': 'datil',
                                                    'tier_ratio': 2
                                                },

                                                {
                                                    'tier_num': 12,
                                                    'tier_pepper': 'habanero',
                                                    'tier_ratio': 2.1
                                                },

                                                {
                                                    'tier_num': 13,
                                                    'tier_pepper': 'ghost chili',
                                                    'tier_ratio': 2.3
                                                },

                                                {
                                                    'tier_num': 14,
                                                    'tier_pepper': 'mace',
                                                    'tier_ratio': 2.4
                                                },

                                                {
                                                    'tier_num': 15,
                                                    'tier_pepper': 'pure capsaicin',
                                                    'tier_ratio': 2.5
                                                },


                                            ],

                            # Commands list
                            "commands": {

                                        "administrator":{
                                                        "tier_number": 0,
                                                        "tier_pepper": 'n00b',
                                                        "altcoms": ['admin'],
                                                        },

                                        "settings":{
                                                        "tier_number": 0,
                                                        "tier_pepper": 'n00b',
                                                        "altcoms": [],
                                                        },

                                        "combat":{
                                                        "tier_number": 0,
                                                        "tier_pepper": 'n00b',
                                                        "altcoms": [],
                                                        },

                                        "author":{
                                                        "tier_number": 0,
                                                        "tier_pepper": 'n00b',
                                                        "altcoms": ['credit','credits'],
                                                        },

                                        "intent":{
                                                        "tier_number": 0,
                                                        "tier_pepper": 'n00b',
                                                        "altcoms": [],
                                                        },

                                        "about":{
                                                        "tier_number": 0,
                                                        "tier_pepper": 'n00b',
                                                        "altcoms": [],
                                                        },

                                        "version":{
                                                        "tier_number": 0,
                                                        "tier_pepper": 'n00b',
                                                        "altcoms": [],
                                                        },

                                        "docs":{
                                                        "tier_number": 0,
                                                        "tier_pepper": 'n00b',
                                                        "altcoms": ['help','man'],
                                                        },

                                        "usage":{
                                                        "tier_number": 0,
                                                        "tier_pepper": 'n00b',
                                                        "altcoms": [],
                                                        },

                                        "travel":{
                                                        "tier_number": 0,
                                                        "tier_pepper": 'n00b',
                                                        "altcoms": [],
                                                        },

                                        # End of commands
                                        },

                            # Alternate Commands, duplicate of above
                            "alt_commands":{

                                            "admin":{
                                                    "realcom": "administrator",
                                                    },

                                            "man":{
                                                    "realcom": "docs",
                                                    },

                                            "help":{
                                                    "realcom": "docs",
                                                    },

                                            "credit":{
                                                    "realcom": "author",
                                                    },

                                            "credits":{
                                                    "realcom": "author",
                                                    },

                                            # end of altcoms
                                            },

                            # end of static content
                            },

                # Current Channel Tier
                "tier_current": 0,

                # Users lists
                "users": {
                            "users_all": [],
                            },

                #
                "playerstats": {},

                # channels list
                "channels": {
                                "game_enabled": [],
                                "devmode_enabled": []

                                },

                # Maps list
                "maps": {

                        "Bouldersummit": {  # 1
                                            "map_size": 10,
                                         },


                        "Cliffstall": {  # 2
                                            "map_size": 11,
                                         },

                        "Whitfield": {  # 3
                                            "map_size": 20,
                                         },

                        "Deepharbor": {  # 4
                                            "map_size": 30,
                                         },

                        "Mightvale": {  # 5
                                            "map_size": 40,
                                         },

                        "Winterkeep": {  # 6
                                            "map_size": 50,
                                         },

                        "Boneshade": {  # 7
                                            "map_size": 60,
                                         },

                        "Faymeadow": {  # 8
                                            "map_size": 70,
                                         },

                        "Bonehollow": {  # 9
                                            "map_size": 80,
                                         },

                        "Honeygulf": {  # 10
                                            "map_size": 90,
                                         },

                        "Rimeshell": {  # 11
                                            "map_size": 110,
                                         },

                        "Wolfbarrow": {  # 12
                                            "map_size": 120,
                                         },

                        "Rivershield": {  # 13
                                            "map_size": 130,
                                         },

                        "Millsummit": {  # 14
                                            "map_size": 140,
                                         },

                        "Dryharbor": {  # 15
                                            "map_size": 150,
                                         },

                        "adminville": {  # admin
                                            "map_size": 150,
                                         }
                        }

                # end of dict
                }


"""
OSD
"""


# How Many characters to put on the display
osd_limit = 420


"""
Github Information
"""


# This Fethes the last modified date from github
rpg_version_plain = '1.5.17'  # If the online check fails
rpg_version_github_page = "https://github.com/SpiceBot/SpiceBot/commits/master/modules/spiceRPG/Game/__init__.py"
rpg_version_github_xpath = '//*[@id="js-repo-pjax-container"]/div[2]/div[1]/div[2]/div[1]/text()'


"""
Activation/Deactivate
"""


onoff_list = ['activate','enable','on','deactivate','disable','off']
activate_list = ['activate','enable','on']
deactivate_list = ['deactivate','disable','off']


"""
Map
"""


rpg_map_center_latitude = "0"
rpg_map_center_longitude = "0"
rpg_map_scale = 10
rpg_map_names = ["adminville"]
rpg_map_namea = ["Bouldersummit",  # 1
                 "Cliffstall",  # 2
                 "Whitfield",  # 3
                 "Deepharbor",  # 4
                 "Mightvale",  # 5
                 "Winterkeep",  # 6
                 "Boneshade",  # 7
                 "Faymeadow",  # 8
                 "Bonehollow",  # 9
                 "Honeygulf",  # 10
                 "Rimeshell",  # 11
                 "Wolfbarrow",  # 12
                 "Rivershield",  # 13
                 "Millsummit",  # 14
                 "Dryharbor"  # 15
                 ]


"""
Commands
"""


# Valid Command Types
rpg_valid_command_types = ['administrator','settings','basic','location','combat']

# Administrator Commands
rpg_commands_valid_administrator = ['administrator']

# User Settings
rpg_commands_valid_settings = ['settings']

# Combat
rpg_commands_valid_combat = ['combat']

# Basic Commands
rpg_commands_valid_basic = ['author','intent','about','version','docs','usage']

# Location
rpg_commands_valid_location = ['travel']


"""
Commands that must be run in channel
"""


rpg_commands_valid_inchannel = []


"""
Commands that can be run with /me
"""


rpg_commands_valid_action = ['combat']

"""
Alternative Commands
"""

# Hotkey
rpg_commands_valid_alt_administrator = ['admin']

# Docs
rpg_commands_valid_alt_docs = ['help','man']

# Hotkey
rpg_commands_valid_alt_hotkey = ['hotlink']

# Author
rpg_commands_valid_alt_author = ['credit','credits']

# settings
rpg_commands_valid_alt_settings = []

# combat
rpg_commands_valid_alt_combat = []

# intent
rpg_commands_valid_alt_intent = []

# about
rpg_commands_valid_alt_about = []

# version
rpg_commands_valid_alt_version = []

# usage
rpg_commands_valid_alt_usage = []

# travel
rpg_commands_valid_alt_travel = []


"""
Command Tiers
"""


rpg_commands_tier_unlocks = [
                            [],  # 1
                            [],  # 2
                            [],  # 3
                            [],  # 4
                            [],  # 5
                            [],  # 6
                            [],  # 7
                            [],  # 8
                            [],  # 9
                            [],  # 10
                            [],  # 11
                            [],  # 12
                            [],  # 13
                            [],  # 14
                            [],  # 15
                            ]

rpg_commands_tier_unlocks_self = [
                                [],  # 1
                                [],  # 2
                                [],  # 3
                                [],  # 4
                                [],  # 5
                                [],  # 6
                                [],  # 7
                                [],  # 8
                                [],  # 9
                                [],  # 10
                                [],  # 11
                                [],  # 12
                                [],  # 13
                                [],  # 14
                                [],  # 15
                                ]


rpg_commands_tier_ratio =    [  1   ,    1.1   ,  1.2   ,   1.3   ,   1.4   ,   1.5    ,   1.6   ,   1.7    ,   1.8   ,   1.9   ,     2       , 2.1   ,   2.2    ,    2.3      , 2.4     ,     2.5        ]  # Tier Ratios
rpg_commands_pepper_levels = ['n00b','pimiento','sonora','anaheim','poblano','jalapeno','serrano','chipotle','tabasco','cayenne','thai pepper','datil','habanero','ghost chili','mace'   ,'pure capsaicin']  # Pepper Levels


"""
Subcommands
"""

# Administrator
subcommands_valid_administrator = ['channel']
subcommands_default_administrator = 0
subcommands_valid_administrator_channel = ['game','devmode']

# settings
subcommands_valid_settings = ['hotkey']
subcommands_default_settings = 0
subcommands_valid_settings_hotkey = ['view','update','reset','list']

# Travel
subcommands_valid_travel = ['north','south','east','west']
subcommands_default_travel = 0


"""
Error messages System
"""


rpg_error_list = ['commands','debug']

rpg_error_debug = [
                    "The Script works at line $list"
]

# Command Run

rpg_error_commands = [
                    "RPG has not been enabled in any bot channels.",  # 1
                    "RPG has not been enabled in $current_chan. The game is enabled in: $game_chans.",  # 2
                    "Which rpg command do you wish to run? Valid Commands include: $valid_coms.",  # 3
                    "Only bot admins may utilize the -a switch.",  # 4
                    "You may only run a unique command once at a time using the multicom feature.",  # 5
                    "The following command(s) do not appear to be valid: $list. Valid commands include: $valid_coms.",  # 6
                    "The following command(s) is/are for admin use only: $list. If you are an admin, you need to run with the -a admin switch.",  # 7
                    "You don't have a command hotlinked to $list",  # 8
                    "It appears that your use of an alternate command failed. $list command(s) were at fault.",  # 9
                    "The Following Command(s) must be used in channel, and do not work via private message: $list",  # 10
                    "$list would kick your butt in a competition.",  # 11
                    "I refuse to fight a biological entity! If I did, you'd be sure to lose!",  # 12
                    "If you are feeling self-destructive, there are places you can call. Alternatively, you can run the harakiri command.",  # 13
                    "Action rpg should not be able to run commands; Targets Only: $list",  # 14
                    "RPG $list will be unlocked at tier(s) $tiers_nums_peppers.",  # 15
                    "RPG $list is for self-use only until tier(s) $tiers_nums_peppers.",  # 16
                    "Your nick is not compatible with playing RPG."  # 17
]

# Configuration

rpg_error_settings = [
                    "Subcommand missing. Valid subcommands include: $valid_subcoms.",  # 1
                    "You cannot adjust settings for other players.",  # 2
                    "The following appear to no be valid RPG players: $list",  # 3
                    "What number would you like to view/modify?",  # 4
                    "You don't appear to have any hotkeys.",  # 5
                    "You don't have a command hotlinked to $list",  # 6
                    "You cannot set an empty hotkey.",  # 7
                    "$list does not appear to be a valid command to hotkey."  # 8
]

rpg_error_administrator = [
                    "Subcommand missing. Valid subcommands include: $valid_subcoms.",  # 1
                    "You must Specify a valid game facet to activate. Valid options include: $valid_game_change",  # 2
                    "You must specify a valid channel. Valid channels include $valid_channels.",  # 3
                    "You must specify toggle status. Valid options include $valid_onoff.",  # 4
                    "RPG devmode is already on in $dev_chans.",  # 5
                    "RPG devmode is already off in $dev_chans.",  # 6
                    "RPG is already on in $game_chans.",  # 7
                    "RPG is already off in $game_chans."  # 8
]

rpg_error_combat = [
                    ""
]

# Basic

rpg_error_author = [
                    ""
]

rpg_error_intent = [
                    ""
]

rpg_error_about = [
                    ""
]

rpg_error_version = [
                    ""
]

rpg_error_docs = [
                    ""
]

rpg_error_usage = [
                    ""
]

rpg_error_travel = [
                    ""
]
