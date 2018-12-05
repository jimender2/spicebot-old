#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import requests
from lxml import html
import datetime
from time import strptime
from dateutil import parser
import calendar
import arrow
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('isup')
def execute_main(bot, trigger):
    checksite = trigger.group(2)
    if not checksite:
        return osd(bot, trigger.sender, 'say', "please enter a site")

    bot.say(str(get_link_status(checksite)))
    return

    if str(checksite).startswith("https://"):
        checksite = checksite.replace("https://", "")
    elif str(checksite).startswith("http://"):
        checksite = checksite.replace("http://", "")

    try:
        page = requests.get("http://" + checksite, headers=header)
        tree = html.fromstring(page.content)
        osd(bot, trigger.sender, 'say', "I am getting a " + str(page.status_code) + " status code for " + str(checksite))
    except Exception as e:
        osd(bot, trigger.sender, 'say', "I am unable to get a status code for " + str(checksite))


def get_link_status(url):

    """
    Gets the HTTP status of the url or returns an error associated with it.  Always returns a string.
    """

    https = False

    url = re.sub(r'(.*)#.*$', r'\1', url)
    url = url.split('/', 3)

    if len(url) > 3:
        path = '/'+url[3]
    else:
        path = '/'

    if url[0] == 'http:':
        port = 80
    elif url[0] == 'https:':
        port = 443
        https = True

    if ':' in url[2]:
        host = url[2].split(':')[0]
        port = url[2].split(':')[1]
    else:
        host = url[2]

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0', 'Host': host}

        if https:
            conn = httplib.HTTPSConnection(host=host, port=port, timeout=10)
        else:
            conn = httplib.HTTPConnection(host=host, port=port, timeout=10)
            conn.request(method="HEAD", url=path, headers=headers)
            response = str(conn.getresponse().status)
            conn.close()

    except socket.gaierror, e:
        response = "Socket Error (%d): %s" % (e[0], e[1])

    except StandardError, e:
        if hasattr(e, 'getcode') and len(e.getcode()) > 0:
            response = str(e.getcode())
        if hasattr(e, 'message') and len(e.message) > 0:
            response = str(e.message)
        elif hasattr(e, 'msg') and len(e.msg) > 0:
            response = str(e.msg)
        elif type('') == type(e):
            response = e
        else:
            response = "Exception occurred without a good error message.  Manually check the URL to see the status.  If it is believed this URL is 100% good then file a issue for a potential bug."
        return response
