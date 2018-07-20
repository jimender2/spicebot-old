#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# pylama:ignore=W,E201,E202,E203,E221,E222,w292

"""
OSD
"""


# How Many characters to put on the display
osd_limit = 420


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
rpg_valid_command_types = ['admin','settings']

# Admin Commands
rpg_commands_valid_admin = ['admin']

# User Settings
rpg_commands_valid_settings = ['settings']

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
Map System
"""


rpg_valid_directions = ['north','south','east','west']


"""
Error messages System
"""


rpg_error_list = ['commands','debug']

rpg_error_debug = [
                    "The Script works at line $list"
]

rpg_error_settings = [
                    "Subcommand missing. Valid subcommands include: $valid_subcoms.",  # 1
                    "You cannot adjust settings for other players.",  # 2
                    "The following appear to no be valid RPG players: $list",  # 3
                    "What number would you like to view/modify?",  # 4
                    "You don't appear to have any hotkeys.",  # 5
                    "You don't have a command hotlinked to $list",  # 6
                    "You can't set an empty hotkey."  # 7
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

rpg_error_commands = [
                    "RPG has not been enabled in any bot channels.",  # 1
                    "RPG has not been enabled in $current_chan. The game is enabled in: $game_chans.",  # 2
                    "Which rpg command do you wish to run? Valid Commands include: $valid_coms.",  # 3
                    "Only bot admins may utilize the -a switch.",  # 4
                    "You may only run a unique command once at a time using the multicom feature.",  # 5
                    "The following command(s) do not appear to be valid: $list. Valid commands include: $valid_coms.",  # 6
                    "The following command(s) is/are for admin use only: $list. If you are an admin, you need to run with the -a admin switch.",  # 7
                    "You don't have a command hotlinked to $list"  # 8
]
