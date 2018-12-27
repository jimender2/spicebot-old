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
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

comdict = {
            "author": "deathbybandaid",
            "contributors": [],
            "description": "",
            'privs': [],
            "example": "",
            "exampleresponse": "",
            }

socialmediadict = {
                  "Instagram": {
                                "url": "https://www.instagram.com/{}",
                                "errorType": "message",
                                "errorMsg": "The link you followed may be broken"
                                },
                  "Twitter": {
                                "url": "https://www.twitter.com/{}",
                                "errorType": "message",
                                "errorMsg": "page doesn’t exist"
                              },
                  "Facebook": {
                                "url": "https://www.facebook.com/{}",
                                "errorType": "status_code"
                              },
                  "YouTube": {
                                "url": "https://www.youtube.com/{}",
                                "errorType": "message",
                                "errorMsg": "Not Found"
                              },
                  "Blogger": {
                                "url": "https://{}.blogspot.com",
                                "errorType": "status_code",
                                "noPeriod": "True"
                              },
                  "Google Plus": {
                                    "url": "https://plus.google.com/+{}",
                                    "errorType": "status_code"
                                  },
                  "Reddit": {
                                "url": "https://www.reddit.com/user/{}",
                                "errorType": "message",
                                "errorMsg": "page not found"
                              },
                  "Pinterest": {
                                "url": "https://www.pinterest.com/{}",
                                "errorType": "response_url",
                                "errorUrl": "https://www.pinterest.com/?show_error=true"
                              },
                  "GitHub": {
                                "url": "https://www.github.com/{}",
                                "errorType": "status_code",
                                "noPeriod": "True"
                              },
                  "Steam": {
                            "url": "https://steamcommunity.com/id/{}",
                            "errorType": "message",
                            "errorMsg": "The specified profile could not be found"
                          },
                  "Vimeo": {
                            "url": "https://vimeo.com/{}",
                            "errorType": "message",
                            "errorMsg": "404 Not Found"
                          },
                  "SoundCloud": {
                                    "url": "https://soundcloud.com/{}",
                                    "errorType": "status_code"
                                  },
                  "Disqus": {
                                "url": "https://disqus.com/{}",
                                "errorType": "status_code"
                              },
                  "Medium": {
                                "url": "https://medium.com/@{}",
                                "errorType": "status_code"
                              },
                  "DeviantART": {
                                    "url": "https://{}.deviantart.com",
                                    "errorType": "status_code",
                                    "noPeriod": "True"
                                  },
                  "VK": {
                            "url": "https://vk.com/{}",
                            "errorType": "status_code"
                          },
                  "About.me": {
                                "url": "https://about.me/{}",
                                "errorType": "status_code"
                              },
                  "Imgur": {
                                "url": "https://imgur.com/user/{}",
                                "errorType": "status_code"
                              },
                  "Flipboard": {
                                "url": "https://flipboard.com/@{}",
                                "errorType": "message",
                                "errorMsg": "loading"
                              },
                  "SlideShare": {
                                "url": "https://slideshare.net/{}",
                                "errorType": "status_code"
                              },
                  "Fotolog": {
                                "url": "https://fotolog.com/{}",
                                "errorType": "status_code"
                              },
                  "Spotify": {
                                "url": "https://open.spotify.com/user/{}",
                                "errorType": "status_code"
                              },
                  "MixCloud": {
                                "url": "https://www.mixcloud.com/{}",
                                "errorType": "message",
                                "errorMsg": "Page Not Found"
                              },
                  "Scribd": {
                                "url": "https://www.scribd.com/{}",
                                "errorType": "message",
                                "errorMsg": "Page not found"
                              },
                  "Patreon": {
                                "url": "https://www.patreon.com/{}",
                                "errorType": "status_code"
                              },
                  "BitBucket": {
                                "url": "https://bitbucket.org/{}",
                                "errorType": "status_code"
                              },
                  "Roblox": {
                                "url": "https://www.roblox.com/user.aspx?username={}",
                                "errorType": "message",
                                "errorMsg": "Page cannot be found or no longer exists"
                              },
                  "Gravatar": {
                                "url": "http://en.gravatar.com/{}",
                                "errorType": "status_code"
                              },
                  "iMGSRC.RU": {
                                "url": "https://imgsrc.ru/main/user.php?user={}",
                                "errorType": "response_url",
                                "errorUrl": "https://imgsrc.ru/"
                              },
                  "DailyMotion": {
                                    "url": "https://www.dailymotion.com/{}",
                                    "errorType": "message",
                                    "errorMsg": "Page not found"
                                  },
                  "Etsy": {
                            "url": "https://www.etsy.com/shop/{}",
                            "errorType": "status_code"
                          },
                  "CashMe": {
                                "url": "https://cash.me/{}",
                                "errorType": "status_code"
                              },
                  "Behance": {
                                "url": "https://www.behance.net/{}",
                                "errorType": "message",
                                "errorMsg": "Oops! We can’t find that page."
                              },
                  "GoodReads": {
                                "url": "https://www.goodreads.com/{}",
                                "errorType": "status_code"
                              },
                  "Instructables": {
                                    "url": "https://www.instructables.com/member/{}",
                                    "errorType": "message",
                                    "errorMsg": "404: We're sorry, things break sometimes"
                                  },
                  "Keybase": {
                                "url": "https://keybase.io/{}",
                                "errorType": "status_code"
                              },
                  "Kongregate": {
                                    "url": "https://www.kongregate.com/accounts/{}",
                                    "errorType": "message",
                                    "errorMsg": "Sorry, no account with that name was found.",
                                    "noPeriod": "True"
                                  },
                  "LiveJournal": {
                                    "url": "https://{}.livejournal.com",
                                    "errorType": "message",
                                    "errorMsg": "Unknown Journal",
                                    "noPeriod": "True"
                                  },
                  "VSCO": {
                            "url": "https://vsco.co/{}",
                            "errorType": "status_code"
                          },
                  "AngelList": {
                                "url": "https://angel.co/{}",
                                "errorType": "message",
                                "errorMsg": "We couldn't find what you were looking for."
                              },
                  "last.fm": {
                                "url": "https://last.fm/user/{}",
                                "errorType": "message",
                                "errorMsg": "Whoops! Sorry, but this page doesn't exist."
                              },
                  "Dribbble": {
                                "url": "https://dribbble.com/{}",
                                "errorType": "message",
                                "errorMsg": "Whoops, that page is gone.",
                                "noPeriod": "True"
                              },
                  "Codecademy": {
                                    "url": "https://www.codecademy.com/{}",
                                    "errorType": "message",
                                    "errorMsg": "404 error"
                                  },
                  "Pastebin": {
                                "url": "https://pastebin.com/u/{}",
                                "errorType": "response_url",
                                "errorUrl": "https://pastebin.com/index"
                              },
                  "Foursquare": {
                                    "url": "https://foursquare.com/{}",
                                    "errorType": "status_code"
                                  },
                  "Gumroad": {
                                "url": "https://www.gumroad.com/{}",
                                "errorType": "message",
                                "errorMsg": "Page not found."
                              },
                  "Newgrounds": {
                                    "url": "https://{}.newgrounds.com",
                                    "errorType": "status_code",
                                    "noPeriod": "True"
                                  },
                  "Wattpad": {
                                "url": "https://www.wattpad.com/user/{}",
                                "errorType": "message",
                                "errorMsg": "This page seems to be missing..."
                              },
                  "Canva": {
                            "url": "https://www.canva.com/{}",
                            "errorType": "message",
                            "errorMsg": "Not found (404)"
                          },
                  "Trakt": {
                            "url": "https://www.trakt.tv/users/{}",
                            "errorType": "message",
                            "errorMsg": "404"
                          },
                  "500px": {
                            "url": "https://500px.com/{}",
                            "errorType": "message",
                            "errorMsg": "Sorry, no such page."
                          },
                  "BuzzFeed": {
                                "url": "https://buzzfeed.com/{}",
                                "errorType": "message",
                                "errorMsg": "We can't find the page you're looking for."
                              },
                  "TripAdvisor": {
                                    "url": "https://tripadvisor.com/members/{}",
                                    "errorType": "message",
                                    "errorMsg": "This page is on vacation…"
                                  },
                  "Contently": {
                                "url": "https://{}.contently.com/",
                                "errorType": "message",
                                "errorMsg": "We can't find that page!",
                                "noPeriod": "True"
                              },
                  "Houzz": {
                                "url": "https://houzz.com/user/{}",
                                "errorType": "message",
                                "errorMsg": "The page you requested was not found."
                              },
                  "BLIP.fm": {
                                "url": "https://blip.fm/{}",
                                "errorType": "message",
                                "errorMsg": "Page Not Found"
                              },
                  "HackerNews": {
                                    "url": "https://news.ycombinator.com/user?id={}",
                                    "errorType": "message",
                                    "errorMsg": "No such user."
                                  },
                  "Codementor": {
                                    "url": "https://www.codementor.io/{}",
                                    "errorType": "message",
                                    "errorMsg": "404"
                                  },
                  "ReverbNation": {
                                    "url": "https://www.reverbnation.com/{}",
                                    "errorType": "message",
                                    "errorMsg": "Sorry, we couldn't find that page"
                                  },
                  "Designspiration": {
                                        "url": "https://www.designspiration.net/{}",
                                        "errorType": "message",
                                        "errorMsg": "Content Not Found"
                                      },
                  "Bandcamp": {
                                "url": "https://www.bandcamp.com/{}",
                                "errorType": "message",
                                "errorMsg": "Sorry, that something isn’t here"
                              },
                  "ColourLovers": {
                                    "url": "https://www.colourlovers.com/love/{}",
                                    "errorType": "message",
                                    "errorMsg": "Page Not Loved"
                                  },
                  "IFTTT": {
                            "url": "https://www.ifttt.com/p/{}",
                            "errorType": "message",
                            "errorMsg": "The requested page or file does not exist"
                          },
                  "Ebay": {
                            "url": "https://www.ebay.com/usr/{}",
                            "errorType": "message",
                            "errorMsg": "The User ID you entered was not found"
                          },
                  "Slack": {
                            "url": "https://{}.slack.com",
                            "errorType": "status_code",
                            "noPeriod": "True"
                          },
                  "Trip": {
                            "url": "https://www.trip.skyscanner.com/user/{}",
                            "errorType": "message",
                            "errorMsg": "Page not found"
                          },
                  "Ello": {
                            "url": "https://ello.co/{}",
                            "errorType": "message",
                            "errorMsg": "We couldn't find the page you're looking for"
                          },
                  "HackerOne": {
                                "url": "https://hackerone.com/{}",
                                "errorType": "message",
                                "errorMsg": "Page not found"
                              },
                  "Tinder": {
                                "url": "https://www.gotinder.com/@{}",
                                "errorType": "message",
                                "errorMsg": "Looking for Someone?"
                              },
                  "We Heart It": {
                                    "url": "https://weheartit.com/{}",
                                    "errorType": "message",
                                    "errorMsg": "Oops! You've landed on a moving target!"
                                  },
                  "Flickr": {
                                "url": "https://www.flickr.com/people/{}",
                                "errorType": "status_code"
                              },
                  "WordPress": {
                                "url": "https://{}.wordpress.com",
                                "errorType": "response_url",
                                "errorUrl": "wordpress.com/typo/?subdomain=",
                                "noPeriod": "True"
                              },
                  "Unsplash": {
                                "url": "https://unsplash.com/@{}",
                                "errorType": "status_code"
                              },
                  "Pexels": {
                                "url": "https://www.pexels.com/@{}",
                                "errorType": "message",
                                "errorMsg": "Ouch, something went wrong!"
                              },
                  "devRant": {
                                "url": "https://devrant.com/users/{}",
                                "errorType": "response_url",
                                "errorUrl": "https://devrant.com/"
                              }
                  }


@sopel.module.commands('username')
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
    bot.say("DBB Testing")

    posstarget = spicemanip(bot, botcom.triggerargsarray, 1) or botcom.instigator
    osd(bot, botcom.channel_current, 'notice', "Checking username " + posstarget)

    data = copy.deepcopy(socialmediadict)

    for social_network in data:
        url = data.get(social_network).get("url").format(username)
        error_type = data.get(social_network).get("errorType")
        cant_have_period = data.get(social_network).get("noPeriod")

        bot.msg("#spicebottest", str(url))
        bot.msg("#spicebottest", str(error_type))
        bot.msg("#spicebottest", str(cant_have_period))


def make_request(url, error_type, social_network):
    try:
        r = requests.get(url, headers=header)
        if r.status_code:
            return r, error_type
    except requests.exceptions.HTTPError as errh:
        print_error(errh, "HTTP Error:", social_network, DEBUG)
    except requests.exceptions.ConnectionError as errc:
        print_error(errc, "Error Connecting:", social_network, DEBUG)
    except requests.exceptions.Timeout as errt:
        print_error(errt, "Timeout Error:", social_network, DEBUG)
    except requests.exceptions.RequestException as err:
        print_error(err, "Unknown error:", social_network, DEBUG)
    return None, ""


def sherlock(username):

    for social_network in data:
        url = data.get(social_network).get("url").format(username)
        error_type = data.get(social_network).get("errorType")
        cant_have_period = data.get(social_network).get("noPeriod")

        if ("." in username) and (cant_have_period == "True"):
            print("\033[37;1m[\033[91;1m-\033[37;1m]\033[92;1m {}:\033[93;1m User Name Not Allowed!".format(social_network))
            continue

        r, error_type = make_request(url=url, error_type=error_type, social_network=social_network)

        if error_type == "message":
            error = data.get(social_network).get("errorMsg")
            # Checks if the error message is in the HTML
            if not error in r.text:
                print("\033[37;1m[\033[92;1m+\033[37;1m]\033[92;1m {}:\033[0m".format(social_network), url)
                write_to_file(url, fname)

            else:
            	print("\033[37;1m[\033[91;1m-\033[37;1m]\033[92;1m {}:\033[93;1m Not Found!".format(social_network))

        elif error_type == "status_code":
            # Checks if the status code of the repsonse is 404
            if not r.status_code == 404:
                print("\033[37;1m[\033[92;1m+\033[37;1m]\033[92;1m {}:\033[0m".format(social_network), url)
                write_to_file(url, fname)

            else:
            	print("\033[37;1m[\033[91;1m-\033[37;1m]\033[92;1m {}:\033[93;1m Not Found!".format(social_network))

        elif error_type == "response_url":
            error = data.get(social_network).get("errorUrl")
            # Checks if the redirect url is the same as the one defined in data.json
            if not error in r.url:
                print("\033[37;1m[\033[92;1m+\033[37;1m]\033[92;1m {}:\033[0m".format(social_network), url)
                write_to_file(url, fname)
            else:
            	print("\033[37;1m[\033[91;1m-\033[37;1m]\033[92;1m {}:\033[93;1m Not Found!".format(social_network))

        elif error_type == "":
            print("\033[37;1m[\033[91;1m-\033[37;1m]\033[92;1m {}:\033[93;1m Error!".format(social_network))

    print("\033[1;92m[\033[0m\033[1;77m*\033[0m\033[1;92m] Saved: \033[37;1m{}\033[0m".format(username+".txt"))
