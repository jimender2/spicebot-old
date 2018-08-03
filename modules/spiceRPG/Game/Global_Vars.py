#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# pylama:ignore=W,E201,E202,E203,E221,E222,w292,E231

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
Commands
"""


# Valid Command Types
rpg_valid_command_types = ['admin','settings','basic']

# Admin Commands
rpg_commands_valid_admin = ['admin']

# User Settings
rpg_commands_valid_settings = ['settings']

# Basic Commands
rpg_commands_valid_basic = ['author','intent','about','version','docs','usage']


"""
Commands that must be run in channel
"""


rpg_commands_valid_inchannel = []


"""
Alternative Commands
"""


# Valid Alternative Commands listing
rpg_commands_valid_alt_types = ['docs','hotkey','author']

# Docs
rpg_commands_valid_alt_docs = ['help','man']

# Hotkey
rpg_commands_valid_alt_hotkey = ['hotlink']

# Author
rpg_commands_valid_alt_author = ['credit','credits']

"""
Subcommands
"""

# Admin
subcommands_valid_admin = ['channel']
subcommands_default_admin = 0
subcommands_valid_admin_channel = ['game','devmode']

# settings
subcommands_valid_settings = ['hotkey']
subcommands_default_settings = 0
subcommands_valid_settings_hotkey = ['view','update','reset','list']


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
                    "The Following Command(s) must be used in channel, and do not work via private message: $list"  # 10
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

rpg_error_admin = [
                    "Subcommand missing. Valid subcommands include: $valid_subcoms.",  # 1
                    "You must Specify a valid game facet to activate. Valid options include: $valid_game_change",  # 2
                    "You must specify a valid channel. Valid channels include $valid_channels.",  # 3
                    "You must specify toggle status. Valid options include $valid_onoff.",  # 4
                    "RPG devmode is already on in $dev_chans.",  # 5
                    "RPG devmode is already off in $dev_chans.",  # 6
                    "RPG is already on in $game_chans.",  # 7
                    "RPG is already off in $game_chans."  # 8
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
