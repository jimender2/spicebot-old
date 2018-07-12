#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

systoolsarray = ["https://sysadmin.it-landscape.info/","https://sysadmin.libhunt.com/","https://github.com/n1trux/awesome-sysadmin","https://docs.microsoft.com/en-us/sysinternals/"]

@sopel.module.commands('sysadmintools')
def execute_main(bot, trigger):
    onscreentext(bot, trigger.sender, systoolsarray)
