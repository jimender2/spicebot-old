import sopel.module
import requests
from xml.dom import minidom
from fake_useragent import UserAgent
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

feednamearray = ['Spiceworks Contests']
urlarray = ['https://community.spiceworks.com/feed/forum/1550.rss']
alturlarray = ['https://community.spiceworks.com/feed/forum/1550.rss']
