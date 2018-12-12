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


@sopel.module.commands('feed', "feeds")
@sopel.module.thread(True)
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

    dispmsg = bot_dictcom_feeds_handler(bot, botcom, "githubrepomaster", True)
    if dispmsg == []:
        osd(bot, botcom.channel_current, 'say', botcom.maincom + " appears to have had an unknown error.")
    else:
        osd(bot, botcom.channel_current, 'say', dispmsg)


def bot_dictcom_feeds_handler(bot, botcom, feed, displayifnotnew=True):

    feed_dict = bot.memory["botdict"]["tempvals"]['feeds'][feed]

    dispmsg = []
    titleappend = False

    url = feed_dict["url"]
    if not url:
        dispmsg.append("URL missing.")
        return dispmsg

    page = requests.get(url, headers=header)
    tree = html.fromstring(page.content)

    if page.status_code == 200:

        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=pytz.UTC)

        displayname = feed_dict["displayname"]

        feed_type = feed_dict["feedtype"]

        if feed_type in ['rss', 'youtube', 'github']:

            lastbuildcurrent = get_nick_value(bot, str(bot.nick), 'long', 'feeds', botcom.maincom + '_lastbuildcurrent') or datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
            lastbuildcurrent = parser.parse(str(lastbuildcurrent))

            xml = page.text
            xml = xml.encode('ascii', 'ignore').decode('ascii')
            xmldoc = minidom.parseString(xml)

            lastbuildtype = feed_dict["lastbuildtype"]

            lastBuildXML = xmldoc.getElementsByTagName(lastbuildtype)

            lastbuildparent = int(feed_dict["lastbuildparent"])

            lastbuildchild = int(feed_dict["lastbuildchild"])

            lastBuildXML = lastBuildXML[lastbuildparent].childNodes[lastbuildchild].nodeValue
            lastBuildXML = parser.parse(str(lastBuildXML))

            if displayifnotnew or lastBuildXML > lastbuildcurrent:

                titleappend = True

                titletype = feed_dict["titletype"]

                titles = xmldoc.getElementsByTagName(titletype)

                titleparent = feed_dict["titleparent"]

                titlechild = int(feed_dict["titlechild"])

                title = titles[titleparent].childNodes[titlechild].nodeValue

                if feed_type == 'github':
                    authors = xmldoc.getElementsByTagName('name')
                    author = authors[0].childNodes[0].nodeValue
                    dispmsg.append(author + " committed")

                title = unicode_string_cleanup(title)

                dispmsg.append(title)

                linktype = feed_dict["linktype"]

                links = xmldoc.getElementsByTagName(linktype)

                linkparent = feed_dict["linkparent"]

                linkchild = feed_dict["linkchild"]

                if str(linkchild).isdigit():
                    linkchild = int(linkchild)
                    link = links[linkparent].childNodes[linkchild].nodeValue.split("?")[0]
                else:
                    link = links[linkparent].getAttribute(linkchild)
                dispmsg.append(link)

                if not displayifnotnew:
                    set_nick_value(bot, str(bot.nick), 'long', 'feeds', botcom.maincom + '_lastbuildcurrent', str(lastBuildXML))

    if titleappend and feed_dict["displayname"]:
        dispmsg.insert(0, "[" + displayname + "]")

    return dispmsg
