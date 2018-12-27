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


@event('001')
@rule('.*')
@sopel.module.thread(True)
def auto_feeds(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["monologue"]):
        pass

    if "feeds" not in bot.memory:
        feed_configs(bot)

    bot_startup_requirements_set(bot, "feeds")

    for feed in bot.memory["feeds"].keys():
        Thread(target=feeds_thread, args=(bot, feed,)).start()


def feeds_thread(bot, feed):
    while True:
        time.sleep(57)
        dispmsg = bot_dictcom_feeds_handler(bot, feed, False)
        if dispmsg != []:

            for channel in bot.privileges.keys():
                feeds_enabled = get_channel_value(bot, channel, "long", "feeds", "enabled") or []
                if feed in feeds_enabled:
                    osd(bot, str(channel), 'say', dispmsg)

            for user in bot.memory["botdict"]["tempvals"]["servers_list"][str(bot.memory["botdict"]["tempvals"]['server'])]['all_current_users']:
                feed_enabled = get_nick_value(bot, user, "long", "feeds", "enabled") or []
                if feed in feed_enabled:
                    osd(bot, user, 'priv', dispmsg)


@sopel.module.commands('feed', "feeds")
@sopel.module.thread(True)
def mainfunction(bot, trigger):

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

    if "feeds" not in bot.memory:
        feed_configs(bot)

    if not len(bot.memory['feeds'].keys()):
        return osd(bot, botcom.channel_current, 'say', "There are no valid feeds!!")

    valid_commands = ['enable', 'disable', 'reset', 'run', 'subscribe', 'unsubscribe']
    command = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_commands], 1) or 'run'
    if command in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(command)

    feed_select = spicemanip(bot, [x for x in botcom.triggerargsarray if x in bot.memory['feeds'].keys() or x == 'all'], 1) or None
    if not feed_select:
        feed_list = spicemanip(bot, bot.memory['feeds'].keys(), 'list')
        osd(bot, botcom.channel_current, 'say', "Valid Feeds are " + feed_list)
        return

    if feed_select == 'all':
        current_feed_list = bot.memory['feeds'].keys()
    else:
        current_feed_list = []
        for word in botcom.triggerargsarray:
            if word in bot.memory['feeds'].keys():
                current_feed_list.append(word)

    if command == 'run':
        for feed in current_feed_list:
            dispmsg = bot_dictcom_feeds_handler(bot, feed, True)
            if dispmsg == []:
                osd(bot, botcom.channel_current, 'say', feed_select + " appears to have had an unknown error.")
            else:
                if feed_select == 'all':
                    osd(bot, botcom.instigator, 'priv', dispmsg)
                else:
                    osd(bot, botcom.channel_current, 'say', dispmsg)
        return

    if command == 'subscribe':
        instigatormodulesarray = get_nick_value(bot, botcom.instigator, "long", "feeds", "enabled") or []
        newlist = []
        for feed in current_feed_list:
            if feed not in instigatormodulesarray:
                newlist.append(feed)
        if newlist != []:
            adjust_nick_array(bot, botcom.instigator, "long", "feeds", "enabled", newlist, "add")
            osd(bot, botcom.channel_current, 'say', "You are now " + command + "d to " + spicemanip(bot, newlist, 'list'))
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    if command == 'unsubscribe':
        instigatormodulesarray = get_nick_value(bot, botcom.instigator, "long", "feeds", "enabled") or []
        newlist = []
        for feed in current_feed_list:
            if feed in instigatormodulesarray:
                newlist.append(feed)
        if newlist != []:
            adjust_nick_array(bot, botcom.instigator, "long", "feeds", "enabled", newlist, "del")
            osd(bot, botcom.channel_current, 'say', "You are now " + command + "d from " + spicemanip(bot, newlist, 'list'))
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    if not bot_command_run_check(bot, botcom, ['admin', 'owner', 'OWNER', 'OP', 'ADMIN']):
        osd(bot, botcom.channel_current, 'say', "Only Bot Admins and Channel Operators are able to adjust Feed settings.")
        return

    if command == 'reset':
        newlist = []
        for feed in current_feed_list:
            feed_type = bot.memory['feeds'][feed]["type"]
            if feed_type in ['rss', 'youtube', 'github', 'redditrss', 'redditapi', 'twitter']:
                newlist.append(feed)
        if newlist != []:
            for feed in newlist:
                reset_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime')
                reset_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle')
                reset_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink')
            osd(bot, botcom.channel_current, 'say', spicemanip(bot, newlist, 'list') + " " + hashave(newlist) + " been " + command + ".")
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    channelselect = spicemanip(bot, [x for x in botcom.triggerargsarray if x in bot.privileges.keys()], 1) or botcom.channel_current

    if command == 'enable':
        feeds_enabled = get_channel_value(bot, channelselect, "long", "feeds", "enabled") or []
        newlist = []
        for feed in current_feed_list:
            if feed not in feeds_enabled:
                newlist.append(feed)
        if newlist != []:
            adjust_channel_array(bot, channelselect, "long", "feeds", "enabled", newlist, "add")
            osd(bot, botcom.channel_current, 'say', spicemanip(bot, newlist, 'list') + " " + hashave(newlist) + " been " + command + "d for " + str(channelselect) + ".")
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    if command == 'disable':
        feeds_enabled = get_channel_value(bot, channelselect, "long", "feeds", "enabled") or []
        newlist = []
        for feed in current_feed_list:
            if feed in feeds_enabled:
                newlist.append(feed)
        if newlist != []:
            adjust_channel_array(bot, channelselect, "long", "feeds", "enabled", newlist, "del")
            osd(bot, botcom.channel_current, 'say', spicemanip(bot, newlist, 'list') + " " + hashave(newlist) + " been " + command + "d for " + str(channelselect) + ".")
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return


def bot_dictcom_feeds_handler(bot, feed, forcedisplay):

    feed_dict = bot.memory['feeds'][feed]

    dispmsg = []
    displayname = False

    now = datetime.datetime.utcnow()
    now = now.replace(tzinfo=pytz.UTC)

    feed_type = feed_dict["type"]

    if feed_type in ['rss', 'youtube', 'github', 'redditrss']:

        url = feed_dict["url"]
        if not url:
            if forcedisplay:
                return ["URL missing."]
            else:
                return []

        page = requests.get(url, headers=header)
        if page.status_code != 200:
            if forcedisplay:
                return ["Recieved http code " + str(page.status_code)]
            else:
                return []

        try:
            feedjson = feedparser.parse(url)
        except Exception as e:
            if forcedisplay:
                return ["No Content Usable."]
            else:
                return []

        lastbuildtime = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime') or datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
        lastbuildtime = parser.parse(str(lastbuildtime))
        try:
            entrytime = feedjson.entries[0].updated
        except Exception as e:
            entrytime = datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
        entrytime = parser.parse(str(entrytime))

        lastbuildtitle = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle') or None
        try:
            title = feedjson.entries[0].title
            title = unicode_string_cleanup(title)
        except Exception as e:
            title = None
        if title:
            dispmsg.append(title)

        lastbuildlink = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink') or None
        try:
            link = feedjson.entries[0].link
        except Exception as e:
            link = None
        if link:
            dispmsg.append(link)

        feedconsensus = []

        if entrytime > lastbuildtime:
            feedconsensus.append('True')
        else:
            feedconsensus.append('False')

        if link != lastbuildlink:
            feedconsensus.append('True')
        else:
            feedconsensus.append('False')

        if title != lastbuildtitle:
            feedconsensus.append('True')
        else:
            feedconsensus.append('False')

        if forcedisplay:
            feedrun = True
        elif 'False' in feedconsensus:
            feedrun = False
        else:
            feedrun = True

        if feedrun:
            displayname = feed_dict["displayname"]
            if not displayname:
                try:
                    displayname = feedjson['feed']['title']
                except Exception as e:
                    displayname = None
        else:
            dispmsg = []

        if not forcedisplay:
            set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime', str(entrytime))
            set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle', str(lastbuildtitle))
            set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink', str(lastbuildlink))

    elif feed_type == 'redditapi':

        url = feed_dict["url"]
        if not url:
            if forcedisplay:
                return ["URL missing."]
            else:
                return []

        page = requests.get(url, headers=header)
        if page.status_code != 200:
            if forcedisplay:
                return ["Recieved http code " + str(page.status_code)]
            else:
                return []

        if not bot.memory["botdict"]["tempvals"]['reddit']:
            if forcedisplay:
                return ["reddit api unavailable."]
            else:
                return []

        path = feed_dict["path"]
        if not path:
            if forcedisplay:
                return ["reddit Path missing."]
            else:
                return []

        currentsubreddit = feed_dict["path"]

        subredditcheck = reddit_subreddit_check(bot, currentsubreddit)
        if not subredditcheck["exists"]:
            if forcedisplay:
                return [subredditcheck["error"]]
            else:
                return []

        try:
            subreddit = bot.memory["botdict"]["tempvals"]['reddit'].subreddit(currentsubreddit)
        except Exception as e:
            if forcedisplay:
                return ["No Content Usable."]
            else:
                return []

        try:
            submissions = subreddit.new(limit=1)
            listarray = []
            for submission in submissions:
                listarray.append(submission)
            submission = listarray[0]
        except Exception as e:
            if forcedisplay:
                return ["No Content Usable."]
            else:
                return []

        lastbuildtime = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime') or datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
        lastbuildtime = parser.parse(str(lastbuildtime))
        try:
            entrytime = submission.created
            entrytime = datetime.datetime.fromtimestamp(entrytime).replace(tzinfo=pytz.UTC)
        except Exception as e:
            entrytime = datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
        entrytime = parser.parse(str(entrytime))

        try:
            submissionscore = str(submission.score)
        except Exception as e:
            submissionscore = None
        if submissionscore:
            dispmsg.append("{" + str(submissionscore) + "}")

        try:
            nsfw = subreddit.over18
        except Exception as e:
            nsfw = False
        if nsfw:
            dispmsg.append("<NSFW>")

        lastbuildtitle = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle') or None
        try:
            title = submission.title
            title = unicode_string_cleanup(title)
        except Exception as e:
            title = None
        if title:
            dispmsg.append(title)

        lastbuildlink = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink') or None
        try:
            link = submission.permalink
        except Exception as e:
            link = None
        if link:
            dispmsg.append(str(feed_dict["url"] + link))

        feedconsensus = []

        if entrytime > lastbuildtime:
            feedconsensus.append('True')
        else:
            feedconsensus.append('False')

        if link != lastbuildlink:
            feedconsensus.append('True')
        else:
            feedconsensus.append('False')

        if title != lastbuildtitle:
            feedconsensus.append('True')
        else:
            feedconsensus.append('False')

        if forcedisplay:
            feedrun = True
        elif 'False' in feedconsensus:
            feedrun = False
        else:
            feedrun = True

        if feedrun:
            displayname = feed_dict["displayname"]
            if not displayname:
                displayname = None
        else:
            dispmsg = []

        if not forcedisplay:
            set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime', str(entrytime))
            set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle', str(lastbuildtitle))
            set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink', str(lastbuildlink))

    elif feed_type == 'twitter':

        url = feed_dict["url"]
        if not url:
            if forcedisplay:
                return ["URL missing."]
            else:
                return []

        page = requests.get(url, headers=header)
        if page.status_code != 200:
            if forcedisplay:
                return ["Recieved http code " + str(page.status_code)]
            else:
                return []

        if not bot.memory["botdict"]["tempvals"]['twitter']:
            if forcedisplay:
                return ["twitter api unavailable."]
            else:
                return []

        handle = feed_dict["handle"]
        if not handle:
            if forcedisplay:
                return ["twitter handle missing."]
            else:
                return []

        currenttweetat = feed_dict["handle"]

        try:
            submissions = bot.memory["botdict"]["tempvals"]['twitter'].GetUserTimeline(screen_name=currenttweetat, count=1, exclude_replies=True, include_rts=False)
            submission = submissions[0]
        except Exception as e:
            if forcedisplay:
                return ["No Content Usable."]
            else:
                return []

        lastbuildtime = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime') or datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
        lastbuildtime = parser.parse(str(lastbuildtime))
        try:
            entrytime = submission.created_at
            entrytime = entrytime.replace(tzinfo=pytz.UTC)
        except Exception as e:
            entrytime = datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
        entrytime = parser.parse(str(entrytime))

        lastbuildtitle = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle') or None
        try:
            title = submission.text
            title = unicode_string_cleanup(title)
        except Exception as e:
            title = None
        if title:
            dispmsg.append(title)

        lastbuildlink = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink') or None
        try:
            link = str(currenttweetat + "/status/" + str(submission.id))
        except Exception as e:
            link = None
        if link:
            dispmsg.append(str(feed_dict["url"] + "/" + link))

        if (entrytime > lastbuildtime and link != lastbuildlink and title != lastbuildtitle) or forcedisplay:
            displayname = feed_dict["displayname"]
            if not displayname:
                displayname = None
        else:
            dispmsg = []

        if not forcedisplay:
            set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime', str(entrytime))
            set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle', str(lastbuildtitle))
            set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink', str(lastbuildlink))

    elif feed_type == 'googlecalendar':

        url = feed_dict["url"]
        if not url:
            if forcedisplay:
                return ["URL missing."]
            else:
                return []

        page = requests.get(url, headers=header)
        if page.status_code != 200:
            if forcedisplay:
                return ["Recieved http code " + str(page.status_code)]
            else:
                return []

        if not bot.memory["botdict"]["tempvals"]['googlecal']:
            if forcedisplay:
                return ["googlecal api unavailable."]
            else:
                return []

        calendar = feed_dict["calendar"]
        if not calendar:
            if forcedisplay:
                return ["google calendar missing."]
            else:
                return []

        currentcalendar = feed_dict["calendar"]

        http_auth = bot.memory["botdict"]["tempvals"]['googlecal'].authorize(httplib2.Http())
        service = build('calendar', 'v3', http=http_auth, cache_discovery=False)

        events_result = service.events().list(timeZone='UTC', calendarId=currentcalendar, maxResults=1, singleEvents=True, orderBy='startTime', timeMin=str(str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "T" + str(now.hour) + ":" + str(now.minute) + ":00.000Z")).execute()
        events = events_result.get('items', [])
        if events == []:
            if forcedisplay:
                return ["No upcoming events on this calendar"]
            else:
                return []
        nextevent = events[0]

        try:
            entrytime = nextevent["start"]["dateTime"]
        except Exception as e:
            entrytime = None
        if not entrytime:
            try:
                entrytime = nextevent["start"]["date"]
            except Exception as e:
                entrytime = None
        if not entrytime:
            if forcedisplay:
                return ["Timestamp Error"]
            else:
                return []
        entrytime = parser.parse(str(entrytime)).replace(tzinfo=pytz.UTC)

        timeuntil = (entrytime - now).total_seconds()
        if timeuntil == 0:
            timecompare = str("Right now")
        elif timeuntil > 0:
            timecompare = humanized_time((entrytime - now).total_seconds())
            timecompare = str(timecompare + " from now")
        else:
            timecompare = humanized_time((now - entrytime).total_seconds())
            timecompare = str(timecompare + " ago")
        # timecompare = arrow_time(now, entrytime)
        dispmsg.append("{Next: " + timecompare + "}")

        try:
            title = nextevent["summary"]
            title = unicode_string_cleanup(title)
        except Exception as e:
            title = None
        if title:
            dispmsg.append(title)

        if not feed_dict["link"]:
            try:
                link = str(nextevent["location"])
                url = findurlsinstring(link)
                if url != []:
                    link = url[0]
                else:
                    link = None
            except Exception as e:
                link = None
            if not link:
                try:
                    link = str(nextevent["description"])
                    url = findurlsinstring(link)
                    if url != []:
                        link = url[0]
                    else:
                        link = None
                except Exception as e:
                    link = None
            if not link:
                try:
                    link = str(nextevent["htmlLink"])
                except Exception as e:
                    link = None
        else:
            link = feed_dict["link"]
        if link:
            dispmsg.append(link)

        if (int(timeuntil) < 900 and int(timeuntil) > 840) or forcedisplay:

            displayname = feed_dict["displayname"]
            if not displayname:
                displayname = None
        else:
            dispmsg = []

    elif feed_type == 'events':

        now = datetime.datetime.utcnow()
        now = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, 0).replace(tzinfo=pytz.UTC)

        entrytime = datetime.datetime(now.year, feed_dict["eventmonth"], feed_dict["eventday"], feed_dict["eventhour"], feed_dict["eventminute"], 0, 0).replace(tzinfo=None)

        feedtimezone = pytz.timezone(feed_dict["timezone"])
        entrytime = feedtimezone.localize(entrytime)
        entrytime = str(entrytime)
        entrytime = parser.parse(entrytime)

        timeuntil = (entrytime - now).total_seconds()
        if timeuntil == 0:
            nextyear = now + datetime.timedelta(days=365)
            nextime = humanized_time((entrytime - now).total_seconds()) + " from now"
            if feed_dict["rightnow"]:
                timecompare = [feed_dict["rightnow"], "(Next): " + nextime]
            else:
                timecompare = ["Right now", "(Next): " + nextime]
        elif timeuntil > 0:
            nextime = humanized_time((entrytime - now).total_seconds()) + " from now"
            lastyear = now - datetime.timedelta(days=365)
            previoustime = humanized_time((now - lastyear).total_seconds()) + " ago"
            timecompare = ["(Previous): " + previoustime, "(Next): " + nextime]
        else:
            previoustime = humanized_time((now - entrytime).total_seconds()) + " ago"
            nextyear = now + datetime.timedelta(days=365)
            nextime = humanized_time((entrytime - now).total_seconds()) + " from now"
            timecompare = ["(Previous): " + previoustime, "(Next): " + nextime]
        dispmsg.extend(timecompare)

        if (int(timeuntil) < 900 and int(timeuntil) > 840) or forcedisplay:

            displayname = feed_dict["displayname"]
            if not displayname:
                displayname = None
        else:
            dispmsg = []

    elif feed_type == 'webinarscrapes':

        url = feed_dict["url"]
        if not url:
            if forcedisplay:
                return ["URL missing."]
            else:
                return []

        page = requests.get(url, headers=header)
        if page.status_code != 200:
            if forcedisplay:
                return ["Recieved http code " + str(page.status_code)]
            else:
                return []

        tree = html.fromstring(page.content)

        scrapetime = feed_dict["scrapetime"]
        scrapetimezone = feed_dict["scrapetimezone"]

        try:
            entrytime = tree.xpath(scrapetime)
            if isinstance(entrytime, list):
                entrytime = entrytime[0]
            entrytime = str(entrytime)
            for r in (("['", ""), ("']", ""), ("\\n", ""), ("\\t", ""), ("@ ", "")):
                entrytime = entrytime.replace(*r)
            entrytime = parser.parse(entrytime)
            if not tz_aware(entrytime):
                feedtimezone = pytz.timezone(feed_dict["scrapetimezone"])
                entrytime = feedtimezone.localize(entrytime)
        except Exception as e:
            if forcedisplay:
                return ["Timestamp Error"]
            else:
                return []

        timeuntil = (entrytime - now).total_seconds()
        if timeuntil == 0:
            timecompare = str("Right now")
        elif timeuntil > 0:
            timecompare = humanized_time((entrytime - now).total_seconds())
            timecompare = str(timecompare + " from now")
        else:
            timecompare = humanized_time((now - entrytime).total_seconds())
            timecompare = str(timecompare + " ago")
        # timecompare = arrow_time(now, entrytime)
        dispmsg.append("{Next: " + timecompare + "}")

        scrapetitle = feed_dict["scrapetitle"]
        if scrapetitle:
            try:
                title = tree.xpath(scrapetitle)
                if isinstance(title, list):
                    title = title[0]
                title = str(title)
                for r in (("u'", ""), ("['", ""), ("[", ""), ("']", ""), ("\\n", ""), ("\\t", "")):
                    title = title.replace(*r)
                title = unicode_string_cleanup(title)
            except Exception as e:
                title = None
            if title:
                dispmsg.append(title)

        scrapelink = feed_dict["scrapelink"]
        if scrapelink:
            try:
                link = tree.xpath(scrapelink)
                if isinstance(link, list):
                    link = link[0]
                link = str(link)
                for r in (("['", ""), ("']", "")):
                    link = link.replace(*r)
                if feed_dict["linkprecede"]:
                    link = str(feed_dict["linkprecede"] + link)
            except Exception as e:
                link = None
            if link:
                dispmsg.append(link)

        scrapebonus = feed_dict["scrapebonus"]
        if scrapebonus:
            try:
                bonus = tree.xpath(scrapebonus)
                if isinstance(bonus, list):
                    bonus = bonus[0]
                bonus = str(bonus)
                scrapebonussplit = feed_dict["scrapebonussplit"]
                if scrapebonussplit:
                    bonus = str(bonus.split(feed_dict["scrapebonussplit"])[-1])
                for r in (("\\r", ""), ("\\n", ""), ("']", ""), ("]", ""), ('"', ''), (" '", ""), ("['", ""), ("[", "")):
                    bonus = bonus.replace(*r)
                bonus = unicode_string_cleanup(bonus)
            except Exception as e:
                bonus = None
            if bonus:
                dispmsg.append(bonus)

        if (int(timeuntil) < 900 and int(timeuntil) > 840) or forcedisplay:

            displayname = feed_dict["displayname"]
            if not displayname:
                displayname = None
        else:
            dispmsg = []

    elif feed_type == 'dailyscrapes':

        url = feed_dict["url"]
        if not url:
            if forcedisplay:
                return ["URL missing."]
            else:
                return []

        page = requests.get(url, headers=header)
        if page.status_code != 200:
            if forcedisplay:
                return ["Recieved http code " + str(page.status_code)]
            else:
                return []

        tree = html.fromstring(page.content)

        try:
            entrytime = datetime.datetime(now.year, now.month, now.day, int(feed_dict["scrapehour"]), int(feed_dict["scrapeminute"]), 0, 0).replace(tzinfo=None)
            entrytime = str(entrytime)
            entrytime = parser.parse(entrytime)
            feedtimezone = pytz.timezone(feed_dict["scrapetimezone"])
            entrytime = feedtimezone.localize(entrytime)
            timeuntil = (entrytime - now).total_seconds()
            if timeuntil < 0:
                tomorrow = now + datetime.timedelta(days=1)
                entrytime = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, int(feed_dict["scrapehour"]), int(feed_dict["scrapeminute"]), 0, 0).replace(tzinfo=None)
                entrytime = str(entrytime)
                entrytime = parser.parse(entrytime)
                feedtimezone = pytz.timezone(feed_dict["scrapetimezone"])
                entrytime = feedtimezone.localize(entrytime)
        except Exception as e:
            if forcedisplay:
                return ["Timestamp Error"]
            else:
                return []

        timeuntil = (entrytime - now).total_seconds()
        timecompare = humanized_time((entrytime - now).total_seconds())
        timecompare = str(timecompare + " from now")
        dispmsg.append("{Next: " + timecompare + "}")

        scrapetitle = feed_dict["scrapetitle"]
        if scrapetitle:
            try:
                title = tree.xpath(scrapetitle)
                if isinstance(title, list):
                    title = title[0]
                title = str(title)
                for r in (("u'", ""), ("['", ""), ("[", ""), ("']", ""), ("\\n", ""), ("\\t", "")):
                    title = title.replace(*r)
                title = unicode_string_cleanup(title)
            except Exception as e:
                title = None
            if title:
                dispmsg.append(title)

        scrapelink = feed_dict["scrapelink"]
        if scrapelink:
            try:
                link = tree.xpath(scrapelink)
                if isinstance(link, list):
                    link = link[0]
                link = str(link)
                for r in (("['", ""), ("']", "")):
                    link = link.replace(*r)
                if feed_dict["linkprecede"]:
                    link = str(feed_dict["linkprecede"] + link)
            except Exception as e:
                link = None
        else:
            link = feed_dict["url"]
        if link:
            dispmsg.append(link)

        if (int(timeuntil) < 0 and int(timeuntil) > -60) or forcedisplay:

            displayname = feed_dict["displayname"]
            if not displayname:
                displayname = None
        else:
            dispmsg = []

    elif feed_type == 'scrapes':

        url = feed_dict["url"]
        if not url:
            if forcedisplay:
                return ["URL missing."]
            else:
                return []

        page = requests.get(url, headers=header)
        if page.status_code != 200:
            if forcedisplay:
                return ["Recieved http code " + str(page.status_code)]
            else:
                return []

        tree = html.fromstring(page.content)

        scrapetime = feed_dict["scrapetime"]
        scrapetimezone = feed_dict["scrapetimezone"]

        try:
            entrytime = tree.xpath(scrapetime)
            if isinstance(entrytime, list):
                entrytime = entrytime[0]
            entrytime = str(entrytime)
            for r in (("['", ""), ("']", ""), ("\\n", ""), ("\\t", ""), ("@ ", "")):
                entrytime = entrytime.replace(*r)
            entrytime = parser.parse(entrytime)
            if not tz_aware(entrytime):
                feedtimezone = pytz.timezone(feed_dict["scrapetimezone"])
                entrytime = feedtimezone.localize(entrytime)
        except Exception as e:
            if forcedisplay:
                return ["Timestamp Error"]
            else:
                return []

        timeuntil = (entrytime - now).total_seconds()
        if timeuntil == 0:
            timecompare = str("Right now")
        elif timeuntil > 0:
            timecompare = humanized_time((entrytime - now).total_seconds())
            timecompare = str(timecompare + " from now")
        else:
            timecompare = humanized_time((now - entrytime).total_seconds())
            timecompare = str(timecompare + " ago")
        # timecompare = arrow_time(now, entrytime)
        dispmsg.append("{Next: " + timecompare + "}")

        scrapetitle = feed_dict["scrapetitle"]
        if scrapetitle:
            try:
                title = tree.xpath(scrapetitle)
                if isinstance(title, list):
                    title = title[0]
                title = str(title)
                for r in (("u'", ""), ("['", ""), ("[", ""), ("']", ""), ("\\n", ""), ("\\t", "")):
                    title = title.replace(*r)
                title = unicode_string_cleanup(title)
            except Exception as e:
                title = None
            if title:
                dispmsg.append(title)

        scrapelink = feed_dict["scrapelink"]
        if scrapelink:
            try:
                link = tree.xpath(scrapelink)
                if isinstance(link, list):
                    link = link[0]
                link = str(link)
                for r in (("['", ""), ("']", "")):
                    link = link.replace(*r)
                if feed_dict["linkprecede"]:
                    link = str(feed_dict["linkprecede"] + link)
            except Exception as e:
                link = None
        else:
            link = feed_dict["url"]
        if link:
            dispmsg.append(link)

        if (int(timeuntil) < 0 and int(timeuntil) > -60) or forcedisplay:

            displayname = feed_dict["displayname"]
            if not displayname:
                displayname = None
        else:
            dispmsg = []

    if displayname and feed_dict["displayname"]:
        dispmsg.insert(0, "[" + displayname + "]")

    botdict_save(bot)
    return dispmsg


def feed_configs(bot):

    bot.memory['feeds'] = dict()

    dirdict = {
                "name": "feeds",
                "dirname": "Feeds",
                }

    filedicts = configs_dir_read(bot, dirdict)

    for dict_from_file in filedicts:

        comconf = dict_from_file["filename"]

        if "type" not in dict_from_file.keys():
            dict_from_file["type"] = quick_coms_type

        if "displayname" not in dict_from_file.keys():
            dict_from_file["displayname"] = None

        if "url" not in dict_from_file.keys():
            dict_from_file["url"] = None

        if dict_from_file["type"] == "redditapi":

            if "path" not in dict_from_file.keys():
                dict_from_file["path"] = None

            if not dict_from_file["url"]:
                dict_from_file["url"] = "https://www.reddit.com"

        if dict_from_file["type"] == "twitter":

            if "handle" not in dict_from_file.keys():
                dict_from_file["handle"] = None

            if not dict_from_file["url"]:
                dict_from_file["url"] = "https://twitter.com"

        if dict_from_file["type"] == "googlecalendar":

            if "calendar" not in dict_from_file.keys():
                dict_from_file["calendar"] = None

            if "link" not in dict_from_file.keys():
                dict_from_file["link"] = None

            if not dict_from_file["url"]:
                dict_from_file["url"] = "https://google.com"

        if dict_from_file["type"] == "dailyscrapes":

            if "scrapetitle" not in dict_from_file.keys():
                dict_from_file["scrapetitle"] = None

            if "scrapehour" not in dict_from_file.keys():
                dict_from_file["scrapehour"] = 1

            if "scrapeminute" not in dict_from_file.keys():
                dict_from_file["scrapeminute"] = 1

            if "scrapetimezone" not in dict_from_file.keys():
                dict_from_file["scrapetimezone"] = "UTC"

            if "scrapelink" not in dict_from_file.keys():
                dict_from_file["scrapelink"] = None

            if "linkprecede" not in dict_from_file.keys():
                dict_from_file["linkprecede"] = None

        if dict_from_file["type"] == "events":

            if "scrapetitle" not in dict_from_file.keys():
                dict_from_file["scrapetitle"] = None

            if "eventmonth" not in dict_from_file.keys():
                dict_from_file["eventmonth"] = 1

            if "eventday" not in dict_from_file.keys():
                dict_from_file["eventday"] = 1

            if "eventhour" not in dict_from_file.keys():
                dict_from_file["eventhour"] = 0

            if "eventminute" not in dict_from_file.keys():
                dict_from_file["eventminute"] = 0

            if "timezone" not in dict_from_file.keys():
                dict_from_file["timezone"] = "UTC"

            if "rightnow" not in dict_from_file.keys():
                dict_from_file["rightnow"] = None

        if dict_from_file["type"] == "scrapes":

            if "scrapetitle" not in dict_from_file.keys():
                dict_from_file["scrapetitle"] = None

            if "scrapetime" not in dict_from_file.keys():
                dict_from_file["scrapetime"] = None

            if "scrapetimezone" not in dict_from_file.keys():
                dict_from_file["scrapetimezone"] = "UTC"

            if "scrapelink" not in dict_from_file.keys():
                dict_from_file["scrapelink"] = None

            if "linkprecede" not in dict_from_file.keys():
                dict_from_file["linkprecede"] = None

        if dict_from_file["type"] == "webinarscrapes":

            if "scrapetime" not in dict_from_file.keys():
                dict_from_file["scrapetime"] = None

            if "scrapetitle" not in dict_from_file.keys():
                dict_from_file["scrapetitle"] = None

            if "scrapelink" not in dict_from_file.keys():
                dict_from_file["scrapelink"] = None

            if "linkprecede" not in dict_from_file.keys():
                dict_from_file["linkprecede"] = None

            if "scrapebonus" not in dict_from_file.keys():
                dict_from_file["scrapebonus"] = None

            if "scrapebonussplit" not in dict_from_file.keys():
                dict_from_file["scrapebonussplit"] = None

            if "scrapetimezone" not in dict_from_file.keys():
                dict_from_file["scrapetimezone"] = "UTC"

        if comconf not in bot.memory['feeds'].keys():
            bot.memory['feeds'][comconf] = dict_from_file


def feed_configs_good(bot):

    feedcount, feedopenfail = 0, 0
    filescan = []
    bot.memory['feeds'] = dict()

    quick_coms_path = bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"] + "Modules/Configs/Feeds/" + str(bot.nick) + "/"
    if os.path.exists(quick_coms_path) and os.path.isdir(quick_coms_path):
        if not os.path.isfile(quick_coms_path) and len(os.listdir(quick_coms_path)) > 0:
            filescan.append(quick_coms_path)

    if "feeds" in bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration'].keys():
        if "extra" in bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration']["feeds"].keys():
            if "," not in str(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration']["feeds"]["extra"]):
                extradirs = [str(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration']["feeds"]["extra"])]
            else:
                extradirs = str(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration']["feeds"]["extra"]).split(",")
            for extra in extradirs:
                quick_coms_path_extra = bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"] + "Modules/Configs/Feeds/" + str(extra) + "/"
                if os.path.exists(quick_coms_path_extra) and os.path.isdir(quick_coms_path_extra):
                    if not os.path.isfile(quick_coms_path_extra) and len(os.listdir(quick_coms_path_extra)) > 0:
                        filescan.append(quick_coms_path_extra)

    # proceed with file iteration
    for directory in filescan:

        # iterate over organizational folder
        for quick_coms_type in os.listdir(directory):
            coms_type_file_path = os.path.join(directory, quick_coms_type)
            if os.path.exists(coms_type_file_path) and not os.path.isfile(coms_type_file_path) and len(os.listdir(coms_type_file_path)) > 0:

                # iterate over files within
                for comconf in os.listdir(coms_type_file_path):
                    comconf_file_path = os.path.join(coms_type_file_path, comconf)

                    if os.path.isfile(comconf_file_path):

                        # Read dictionary from file, if not, enable an empty dict
                        filereadgood = True
                        inf = codecs.open(os.path.join(coms_type_file_path, comconf), "r", encoding='utf-8')
                        infread = inf.read()
                        try:
                            dict_from_file = eval(infread)
                        except Exception as e:
                            filereadgood = False
                            stderr("Error loading feed %s: %s (%s)" % (comconf, e, comconf_file_path))
                            dict_from_file = dict()
                        # Close File
                        inf.close()

                        if filereadgood and isinstance(dict_from_file, dict):

                            feedcount += 1

                            if "type" not in dict_from_file.keys():
                                dict_from_file["type"] = quick_coms_type

                            if "displayname" not in dict_from_file.keys():
                                dict_from_file["displayname"] = None

                            if "url" not in dict_from_file.keys():
                                dict_from_file["url"] = None

                            if dict_from_file["type"] == "redditapi":

                                if "path" not in dict_from_file.keys():
                                    dict_from_file["path"] = None

                                if not dict_from_file["url"]:
                                    dict_from_file["url"] = "https://www.reddit.com"

                            if dict_from_file["type"] == "twitter":

                                if "handle" not in dict_from_file.keys():
                                    dict_from_file["handle"] = None

                                if not dict_from_file["url"]:
                                    dict_from_file["url"] = "https://twitter.com"

                            if dict_from_file["type"] == "googlecalendar":

                                if "calendar" not in dict_from_file.keys():
                                    dict_from_file["calendar"] = None

                                if "link" not in dict_from_file.keys():
                                    dict_from_file["link"] = None

                                if not dict_from_file["url"]:
                                    dict_from_file["url"] = "https://google.com"

                            if dict_from_file["type"] == "dailyscrapes":

                                if "scrapetitle" not in dict_from_file.keys():
                                    dict_from_file["scrapetitle"] = None

                                if "scrapehour" not in dict_from_file.keys():
                                    dict_from_file["scrapehour"] = 1

                                if "scrapeminute" not in dict_from_file.keys():
                                    dict_from_file["scrapeminute"] = 1

                                if "scrapetimezone" not in dict_from_file.keys():
                                    dict_from_file["scrapetimezone"] = "UTC"

                                if "scrapelink" not in dict_from_file.keys():
                                    dict_from_file["scrapelink"] = None

                                if "linkprecede" not in dict_from_file.keys():
                                    dict_from_file["linkprecede"] = None

                            if dict_from_file["type"] == "events":

                                if "scrapetitle" not in dict_from_file.keys():
                                    dict_from_file["scrapetitle"] = None

                                if "eventmonth" not in dict_from_file.keys():
                                    dict_from_file["eventmonth"] = 1

                                if "eventday" not in dict_from_file.keys():
                                    dict_from_file["eventday"] = 1

                                if "eventhour" not in dict_from_file.keys():
                                    dict_from_file["eventhour"] = 0

                                if "eventminute" not in dict_from_file.keys():
                                    dict_from_file["eventminute"] = 0

                                if "timezone" not in dict_from_file.keys():
                                    dict_from_file["timezone"] = "UTC"

                                if "rightnow" not in dict_from_file.keys():
                                    dict_from_file["rightnow"] = None

                            if dict_from_file["type"] == "scrapes":

                                if "scrapetitle" not in dict_from_file.keys():
                                    dict_from_file["scrapetitle"] = None

                                if "scrapetime" not in dict_from_file.keys():
                                    dict_from_file["scrapetime"] = None

                                if "scrapetimezone" not in dict_from_file.keys():
                                    dict_from_file["scrapetimezone"] = "UTC"

                                if "scrapelink" not in dict_from_file.keys():
                                    dict_from_file["scrapelink"] = None

                                if "linkprecede" not in dict_from_file.keys():
                                    dict_from_file["linkprecede"] = None

                            if dict_from_file["type"] == "webinarscrapes":

                                if "scrapetime" not in dict_from_file.keys():
                                    dict_from_file["scrapetime"] = None

                                if "scrapetitle" not in dict_from_file.keys():
                                    dict_from_file["scrapetitle"] = None

                                if "scrapelink" not in dict_from_file.keys():
                                    dict_from_file["scrapelink"] = None

                                if "linkprecede" not in dict_from_file.keys():
                                    dict_from_file["linkprecede"] = None

                                if "scrapebonus" not in dict_from_file.keys():
                                    dict_from_file["scrapebonus"] = None

                                if "scrapebonussplit" not in dict_from_file.keys():
                                    dict_from_file["scrapebonussplit"] = None

                                if "scrapetimezone" not in dict_from_file.keys():
                                    dict_from_file["scrapetimezone"] = "UTC"

                            if comconf not in bot.memory['feeds'].keys():
                                bot.memory['feeds'][comconf] = dict_from_file
                        else:
                            feedopenfail += 1
    if feedcount > 1:
        stderr('\n\nRegistered %d feed files,' % (feedcount))
        stderr('%d feed files failed to load\n\n' % feedopenfail)
    else:
        stderr("Warning: Couldn't load any feed files")

    bot.memory["botdict"]["tempvals"]['feed_count'] = feedcount
