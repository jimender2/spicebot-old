import sopel
import random

@sopel.module.rate(120)
@sopel.module.commands('8ball')
def ball(bot, trigger):
    bot.say("Let me dig deep into the waters of life, and find your answer")
    responses  = ["Only on Tuesdays","42","Not so sure","Negative", "Could be", "Unclear, ask again", "Yes", "No", "Possible, but not probable","Most likely","Absolutely not","I see good things happening","Never","Outlook is good","It is certain"," It is decidedly so","Without a doubt","Yes definitely","You may rely on it","As I see it yes","Most likely","Outlook good","Yes","Signs point to yes","Reply hazy try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","God says no","Very doubtful","Outlook not so good"]
    reply = random.randint(0,len(responses) - 1)
    bot.say(responses [reply]);
