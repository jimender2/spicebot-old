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
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


"""
This will display a link to the online wiki for the bot
"""


@nickname_commands('help', 'docs')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    osd(bot, trigger.nick, 'say', ["IRC Modules Repository", str(github_dict["url_main"] + github_dict["repo_owner"] + "/" + github_dict["repo_name"] + github_dict["url_path_wiki"])])