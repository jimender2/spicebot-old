import sopel.module
import random

@sopel.module.rate(120)
@sopel.module.commands('cipher','terminator','ciphertheterminator')
def cipher(bot, trigger):
    missiontypes  = ["Terminate","Protect","Skynet"]
    missiontype = random.randint(0,len(missiontypes) - 1)
    missiontype = str(missiontypes [missiontype])
    mission = str(missiontype)
    
    if missiontype == 'Skynet':
        missions  = ["ENSURE THE ACTIVATION OF SKYNET","PRESERVE THE CREATION OF SKYNET","PRESERVE THE CREATION OF ARTIE","ENSURE THE CREATION OF GENISYS"]
        mission = random.randint(0,len(missions) - 1)
        mission = str(missions [mission])
        
    elif missiontype == 'Terminate':
        missions  = ["Sarah Connor","John Connor","Kyle Reese","Mary Warren","Marco Cassetti","Kate Brewster","Robert Brewster","Elizabeth Anderson","William Anderson","Jose Barrera","Simon Taylor","Isaac Hall","Fritz Roland","Ted Snavely","Sharlene Gen","Vince Forcer",]
        mission = random.randint(0,len(missions) - 1)
        mission = str('TERMINATE' + mission)
        mission = str(missions [mission])
        
    elif missiontype == 'Protect':
        missions  = ["PROTECT Sarah Connor","PROTECT John Connor","ENSURE THE SURVIVAL OF John Connor AND Katherine Brewster"]
        mission = random.randint(0,len(missions) - 1)
        mission = str(missions [mission])
        
    bot.say('CYBORG TISSUE GENERATION 800 SERIES MODEL 101 SEQUENCE INITIATED')
    bot.say('DOWNLOADING CURRENT OBJECTIVE FROM SKYNET: ' + str(mission))
    bot.say('ACTIVATING Cipher-0')
