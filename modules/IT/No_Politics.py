#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os

@sopel.module.commands('sign','politics','religion')
def execute_main(bot, trigger):
    bot.say("NO POLITICS OR RELIGION IN #spiceworks!")
