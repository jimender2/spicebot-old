import sopel.module
import random

@sopel.module.rate(120)
@sopel.module.commands('cipher','terminator','ciphertheterminator')
def cipher(bot, trigger):
    if not trigger.group(2):
        modelnumbers  = ["T-1 SERIES","T-70 SERIES","T-600 SERIES","T-700 SERIES","T-1001 SERIES","T-888 SERIES","TOK715 SERIES","T-X SERIES","T-1000 SERIES","T-800 SERIES, Model 101","T-850 SERIES"]
        modelnumber = random.randint(0,len(modelnumbers) - 1)
        modelnumber = str(modelnumbers [modelnumber])
        modelnumber = str(modelnumber)
    
        missiontypes  = ["Terminate","Protect","Skynet","Spice"]
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
            mission = str(missions [mission])
            mission = str('TERMINATE ' + mission)
        
        elif missiontype == 'Protect':
            missions  = ["PROTECT Sarah Connor","PROTECT John Connor","ENSURE THE SURVIVAL OF John Connor AND Katherine Brewster"]
            mission = random.randint(0,len(missions) - 1)
            mission = str(missions [mission])
        
        elif missiontype == 'Spice':
            missions  = ["Protect Technical Angel","INSTALL MOAR PATCHES"]
            mission = random.randint(0,len(missions) - 1)
            mission = str(missions [mission])
        
        bot.say('CYBORG TISSUE GENERATION ' + str(modelnumber) + ' SEQUENCE INITIATED')
        bot.say('DOWNLOADING CURRENT OBJECTIVE FROM SKYNET: ' + str(mission))
        bot.say('ACTIVATING Cipher-0')

    else:
        if trigger.group(2) == 'story':
            bot.say('The machines rose from the ashes of the nuclear fire. Their war to exterminate mankind had raged on for decades. But the final battle will not be fought in the future. It would be fought in our present...tonight.')
        elif trigger.group(2) == 'Cipher-0':
            if 'Cipher-0' not in bot.privileges[channel.lower()]:
                bot.say('It appears that Cipher-0 is not reachable.')
            else:
                bot.say('It appears that Cipher-0 is currently activated.')
