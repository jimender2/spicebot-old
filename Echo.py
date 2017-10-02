import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('echo','echo','echo')
def echo(bot,trigger):
    bot.say(".echo")
