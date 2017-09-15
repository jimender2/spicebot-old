import sopel.module
import subprocess

@sopel.module.commands('debug')
def debug(bot, trigger):
    status = subprocess.check_output("sudo service sopel status", shell=True)
    bot.say(status)
