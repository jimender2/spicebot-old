import sopel.module
import os
import sys
from os.path import exists

script_dir = os.path.dirname(__file__)
rel_path = "templog.txt"
abs_file_path = os.path.join(script_dir, rel_path)

@sopel.module.require_admin
@sopel.module.commands('debug')
def debug(bot, trigger):
    bot.action('Is Copying Log')
    os.system("sudo journalctl -u sopel >> " + abs_file_path)
    bot.action('Is Filtering Log')
    os.system("sudo sed -i '/Starting Sopel IRC bot/h;//!H;$!d;x;' " + abs_file_path)
    os.system("sudo sed -i '/sudo/d; /COMMAND/d' " + abs_file_path)
    for line in open(abs_file_path):
        bot.say(line)
    if os.path.getsize(abs_file_path) == 0:
        bot.say(Log File Not Updated.)
    bot.action('Is Removing Log')
    os.system("sudo rm " + abs_file_path)
