#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module


# imports for system and OS access, directories
import os
import sys

# imports based on THIS file
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

comdict = {
            "author": "deathbybandaid",
            "contributors": [],
            "description": "",
            'privs': [],
            "example": "",
            "exampleresponse": "",
            }


@sopel.module.commands('cipher', 'terminator', 'ciphertheterminator')
def mainfunctionnobeguine(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    if not botcom.multiruns:
        execute_main(bot, trigger, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    terminatordict = {

                        "story": [
                                    'The machines rose from the ashes of the nuclear fire.',
                                    'Their war to exterminate mankind had raged on for decades.',
                                    'But the final battle will not be fought in the future.',
                                    'It would be fought in our present...tonight.',
                                    ],

                        "modelnumbers": [
                                        "T-1 SERIES",
                                        "T-70 SERIES",
                                        "T-600 SERIES",
                                        "T-700 SERIES",
                                        "T-1001 SERIES",
                                        "T-888 SERIES",
                                        "TOK715 SERIES",
                                        "T-X SERIES",
                                        "T-1000 SERIES",
                                        "T-800 SERIES, Model 101",
                                        "T-850 SERIES",
                                        ],

                        "missiontypes": {

                                        "terminate": {
                                                        [
                                                            "Sarah Connor",
                                                            "John Connor",
                                                            "Kyle Reese",
                                                            "Mary Warren",
                                                            "Marco Cassetti",
                                                            "Kate Brewster",
                                                            "Robert Brewster",
                                                            "Elizabeth Anderson",
                                                            "William Anderson",
                                                            "Jose Barrera",
                                                            "Simon Taylor",
                                                            "Isaac Hall",
                                                            "Fritz Roland",
                                                            "Ted Snavely",
                                                            "Sharlene Gen",
                                                            "Vince Forcer",
                                                            ],
                                                        },

                                        "protect": {
                                                        [
                                                            "PROTECT Sarah Connor",
                                                            "PROTECT John Connor",
                                                            "ENSURE THE SURVIVAL OF John Connor AND Katherine Brewster",
                                                            ],
                                                    },

                                        "skynet": {
                                                    [
                                                        "ENSURE THE ACTIVATION OF SKYNET",
                                                        "PRESERVE THE CREATION OF SKYNET",
                                                        "PRESERVE THE CREATION OF ARTIE",
                                                        "ENSURE THE CREATION OF GENISYS",
                                                    ]
                                                    },

                                        "spice": {
                                                    [
                                                        "Protect Technical Angel",
                                                        "INSTALL MOAR PATCHES",
                                                        ],
                                                },
                                        },
                        }

    target = spicemanip(bot, triggerargsarray, 1) or None

    if (bot_check_inlist(bot, botcom.instigator, str('Cipher-0')) and not target) or target == 'Cipher-0':

        modelnumber = spicemanip(bot, terminatordict["modelnumbers"], 'random').upper()

        missiontype = spicemanip(bot, terminatordict["missiontypes"], 'random')

        mission = spicemanip(bot, terminatordict["missiontypes"][missiontype], 'random').upper()

        osd(bot, botcom.channel_current, 'say', 'CYBORG TISSUE GENERATION ' + modelnumber + ' SEQUENCE INITIATED')

        osd(bot, botcom.channel_current, 'say', 'DOWNLOADING CURRENT OBJECTIVE FROM SKYNET: ' + mission)

        osd(bot, botcom.channel_current, 'say', 'ACTIVATING Cipher-0')

    elif not target:
        osd(bot, botcom.channel_current, 'say', 'Pinging Cipher-0 with a WOL packet...')

    elif target == 'story':
        osd(bot, botcom.channel_current, 'say', terminatordict["story"])
