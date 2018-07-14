#!/usr/bin/env python
# coding=utf-8
import os


def save():
    # write buffer to the file
    f.flush()
    os.fsync(f.fileno())


fileName = raw_input("What do you want to name the file?")
unstrippedcommands = raw_input("What do you want the commands to be?")
author = raw_input("Who is the author?")

fileLocation = "SpiceBot\\development\\" + fileName + ".py"
print "creating module"
f = open(fileLocation, 'w')
f.write("test")
