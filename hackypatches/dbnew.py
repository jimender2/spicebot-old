# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

##################################################################################################
## This is an attempt to bridge the gap between Sopel and Willie in regards to database support ##
## sqlite seems to not be capable of handling what SpiceBot needs it to                         ##
##################################################################################################

import os
import json
import os.path
import sys
from sopel.tools import Identifier

if sys.version_info.major >= 3:
    unicode = str
    basestring = str
    
# def _deserialize(value)   goes here
    
    
    
class SopelDB(object):
    







