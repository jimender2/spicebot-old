import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

import speedtest


@sopel.module.require_admin
@sopel.module.commands('speedtest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    osd(bot, trigger.sender, 'say', "Starting Speedtest...")

    servers = []
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download()
    s.upload()
    s.results.share()
    results_dict = s.results.dict()
    osd(bot, trigger.sender, 'say', str(results_dict['client']['share']))


"""
{
'client': {
            'rating': '0',
            'loggedin': '0',
            'isprating': '3.7',
            'ispdlavg': '0',
            'ip': '131.93.141.62',
            'isp': 'Spectrum',
            'lon': '-87.4545',
            'ispulavg': '0',
            'country': 'US',
            'lat': '46.5786'},
            'bytes_sent': 27918336,
            'download': 159917730.11941049,
            'timestamp': '2018-10-23T13:39:28.056531Z',
            'share': u'http://www.speedtest.net/result/7740317974.png',
            'bytes_received': 200888412,
            'ping': 61.299,
            'upload': 22144728.947812572,
            'server': {
                        'latency': 61.299,
                        'name': 'Houghton, MI',
                        'url': 'http://208.68.24.149/speedtest/upload.php',
                        'country': 'United States',
                        'lon': '-88.5689',
                        'cc': 'US',
                        'host': 'speedtest.remc1.net:8080',
                        'sponsor': 'REMC1',
                        'url2': 'http://speedtest.remc1.net/speedtest/upload.php',
                        'lat': '47.1219',
                        'id': '5207',
                        'd': 104.07353745240147
                        }
            }
"""
