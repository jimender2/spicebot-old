#!/usr/bin/env python
# coding=utf-8
import os

"""
Cool idea, but I see some issues going in - deathbybandaid
"""


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

f.write("#!/usr/bin/env python\n# coding=utf-8\n")
f.write("from __future__ import unicode_literals, absolute_import, print_function, division\n")
f.write("import sopel.module\nimport sys\nimport os\nmoduledir = os.path.dirname(__file__)\n")
f.write("shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))\n")
f.write("sys.path.append(shareddir)\nfrom BotShared import *\n\n")

authorline = "# author " + author
f.write("authorline")
