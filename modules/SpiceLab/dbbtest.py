#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

import subprocess


@sopel.module.commands('dbbtest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    commands_array = spicemanip(bot, triggerargsarray, "split_&&")
    if commands_array == []:
        commands_array = [[]]
    for command_split_partial in commands_array:
        triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
        execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    osd(bot, trigger.sender, 'say', "This is deathbybandaid's test module")
    osdtest = []

    cmd = '/bin/systemctl status %s.service' % "SpiceBot"
    # proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    # stdout_list = proc.communicate()[0].split('\n')
    # for line in stdout_list:
    #    osdtest.append(str(line))

    proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    outs, errs = proc.communicate(timeout=15)
    for line in outs:
        osdtest.append(str(line))

    for line in errs:
        osdtest.append(str(line))

    for line in osdtest:
        osd(bot, trigger.sender, 'say', line)
