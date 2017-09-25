import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('sysadmintools')
def sysadmintools(bot, trigger):
    bot.say('https://sysadmin.it-landscape.info/     https://sysadmin.libhunt.com/     https://github.com/n1trux/awesome-sysadmin')
