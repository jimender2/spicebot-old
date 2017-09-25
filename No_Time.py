import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('notime')
def notime(bot,trigger):
    bot.say("Well I woke up to get me a cold pop and then I thought somebody was barbequing. I said oh lord Jesus it's a fire. Then I ran out, I didn't grab no shoes or nothin' Jesus, I ran for my life. And then the smoke got me, I got bronchitis ain't nobody got time for that.")
