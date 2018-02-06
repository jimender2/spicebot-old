
### Duels Old
def getreadytorumble(bot, trigger, instigator, targetarray, OSDTYPE, fullcommandused, now, triggerargsarray, typeofduel, channel):
    

    assaultstatsarray = ['wins','losses','potionswon','potionslost','kills','deaths','damagetaken','damagedealt','levelups','xp']
    getreadytorumblenamearray = ['nicktitles','nickpepper','nickmagicattributes','nickarmor']
    ## clean empty stats
    assaultdisplay = ''
    assault_xp, assault_wins, assault_losses, assault_potionswon, assault_potionslost, assault_deaths, assault_kills, assault_damagetaken, assault_damagedealt, assault_levelups = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    targetarraytotal = len(targetarray)
    for target in targetarray:
        targetarraytotal = targetarraytotal - 1
        
        ## Cleanup
        combattextarraycomplete = []
        texttargetarray = []
        
        ## Assault does not touch lastfought
        if typeofduel == 'assault':
            targetlastfoughtstart = get_database_value(bot, target, 'lastfought')
        
        ## Same person can't instigate twice in a row
        set_database_value(bot, bot.nick, 'lastinstigator', instigator)
        
        ## Update last fought
        if instigator != target:
            set_database_value(bot, instigator, 'lastfought', target)
            set_database_value(bot, target, 'lastfought', instigator)
        
        ## Update Time Of Combat
        set_database_value(bot, instigator, 'timeout', now)
        set_database_value(bot, target, 'timeout', now)
        set_database_value(bot, bot.nick, 'timeout', now)
        
        ## Starting Tier
        currenttierstart = get_database_value(bot, bot.nick, 'levelingtier') or 0

        ## Magic Attributes Start
        instigatorshieldstart, targetshieldstart, instigatorcursestart, targetcursestart = get_current_magic_attributes(bot, instigator, target)

        ## Display Naming
        instigatorname = ''
        targetname = ''
        instigatorpepperstart = get_pepper(bot, instigator)
        for q in getreadytorumblenamearray:
            instigatorscriptdef = str(q + "(bot, instigator, channel)")
            instigatornameadd = eval(instigatorscriptdef)
            instigatornameadd = str(instigatornameadd)
            if instigatorname == '':
                instigatorname = str(instigatornameadd)
            else:
                instigatorname = str(instigatorname + " " + instigatornameadd)
        if instigator == target:
            targetname = "themself"
            targetpepperstart = ''
        else:
            targetpepperstart = get_pepper(bot, target)
            for q in getreadytorumblenamearray:
                targetscriptdef = str(q + "(bot, target, channel)")
                targetnameadd = eval(targetscriptdef)
                targetnameadd = str(targetnameadd)
                if targetname == '':
                    targetname = str(targetnameadd)
                else:
                    targetname = str(targetname + " " + targetnameadd)

        ## Announce Combat
        announcecombatmsg = str(instigatorname + " versus " + targetname)
        combattextarraycomplete.append(announcecombatmsg)
            
        ## Chance of Instigator finding loot
        lootwinnermsg = ''
        randominventoryfind = randominventory(bot, instigator)
        if randominventoryfind == 'true' and target != bot.nick and instigator != target:
            loot = get_trigger_arg(potion_types, 'random')
            loot_text = eval(loot+"dispmsg")
            lootwinnermsg = str(instigator + ' found a ' + str(loot) + ' ' + str(loot_text))
            combattextarraycomplete.append(lootwinnermsg)
        
        ## Select Winner
        if target == bot.nick:
            winner = bot.nick
            loser = instigator
        else:
            nickarray = [instigator, target]
            winner = selectwinner(bot, nickarray)
            if winner == instigator:
                loser = target
            else:
                loser = instigator
        
        ## classes
        yourclasswinner = get_database_value(bot, winner, 'class') or 'notclassy'
        yourclassloser = get_database_value(bot, loser, 'class') or 'notclassy'
        
        ## Current Streaks
        winner_loss_streak, loser_win_streak = get_current_streaks(bot, winner, loser)

        ## Update Wins and Losses
        if instigator != target:
            adjust_database_value(bot, winner, 'wins', 1)
            adjust_database_value(bot, loser, 'losses', 1)
            set_current_streaks(bot, winner, 'win')
            set_current_streaks(bot, loser, 'loss')
        
        ## Manual weapon
        weapon = get_trigger_arg(triggerargsarray, '2+')
        if winner == instigator and weapon and currenttierstart >= tierunlockweaponslocker:
            if weapon == 'all':
                weapon = getallchanweaponsrandom(bot)
            elif weapon == 'target':
                weapon = weaponofchoice(bot, target)
                weapon = str(target + "'s " + weapon)
        elif winner == bot.nick:
            weapon = ''
        else:
            weapon = weaponofchoice(bot, winner)
        weapon = weaponformatter(bot, weapon)
        if weapon != '':
            weapon = str(" " + weapon)
        
        ## Combat Process
        damage, winnermsgarray, assault_kills, assault_deaths = damagedone(bot, winner, loser, instigator, weapon, 1, assault_kills, assault_deaths)
        for x in winnermsgarray:
            combattextarraycomplete.append(x)
            
        ## Update Health Of Loser, respawn, allow winner to loot
        losercurrenthealth = get_database_value(bot, loser, 'health')
        if instigator == target:
            loser = targetname
        if losercurrenthealth <= 0:
            if winner == loser:
                deathmsgb = suicidekill(bot,loser)
            else:
                deathmsgb = whokilledwhom(bot, winner, loser) or ''
            winnermsg = str(loser + ' dies forcing a respawn!!')
            if winner == instigator:
                assault_kills = assault_kills + 1
            else:
                assault_deaths = assault_deaths + 1
            combattextarraycomplete.append(winnermsg)
            if deathmsgb != '':
                combattextarraycomplete.append(deathmsgb)
        
        ## Knight/Paladin
        winnercurrenthealth = get_database_value(bot, winner, 'health')
        if winnercurrenthealth <= 0 and winner != loser:
            deathmsgb = whokilledwhom(bot, winner, loser) or ''
            
        
        
        ## Chance that Instigator looses found loot
        if randominventoryfind == 'true' and target != bot.nick and instigator != target:
            lootwinnermsgb = ''
            ## Barbarians get a 50/50 chance of getting loot even if they lose
            classloser = get_database_value(bot, loser, 'class') or 'notclassy'
            barbarianstealroll = randint(0, 100)
            if classloser == 'barbarian' and barbarianstealroll >= 50:
                lootwinnermsgb = str(loser + " steals the " + str(loot))
                lootwinner = loser
            elif winner == target:
                lootwinnermsgb = str(winner + " gains the " + str(loot))
                lootwinner = winner
            else:
                lootwinner = winner
            adjust_database_value(bot, lootwinner, loot, 1)
            if lootwinner == instigator:
                assault_potionswon = assault_potionswon + 1
            else:
                assault_potionslost = assault_potionslost + 1
            if lootwinnermsgb != '':
                combattextarraycomplete.append(lootwinnermsgb)

        ## Update XP points
        if yourclasswinner == 'ranger':
            XPearnedwinner = xp_winner_ranger
        else:
            XPearnedwinner = xp_winner
        if yourclassloser == 'ranger':
            XPearnedloser = xp_loser_ranger
        else:
            XPearnedloser = xp_loser
        if instigator != target:
            winnertier = get_database_value(bot, winner, 'levelingtier')
            losertier = get_database_value(bot, loser, 'levelingtier')
            xptier = tierratio_level(bot)
            if winnertier < currenttierstart:
                XPearnedwinner = XPearnedwinner * xptier
            if losertier < currenttierstart:
                XPearnedloser = XPearnedloser * xptier
            adjust_database_value(bot, winner, 'xp', XPearnedwinner)
            adjust_database_value(bot, loser, 'xp', XPearnedloser)
        
        ## new pepper level?
        instigatorpeppernow = get_pepper(bot, instigator)
        if instigatorpeppernow != instigatorpepperstart and instigator != target:
            pepperstatuschangemsg = str(instigator + " graduates to " + instigatorpeppernow + "! ")
            assault_levelups = assault_levelups + 1
            combattextarraycomplete.append(pepperstatuschangemsg)
        targetpeppernow = get_pepper(bot, target)
        if targetpeppernow != targetpepperstart and instigator != target:
            pepperstatuschangemsg = str(target + " graduates to " + targetpeppernow + "! ")
            combattextarraycomplete.append(pepperstatuschangemsg)
        
        ## Tier update
        tierchangemsg = ''
        currenttierend = get_database_value(bot, bot.nick, 'levelingtier') or 1
        if int(currenttierend) > int(currenttierstart):
            tierchangemsg = str("New Tier Unlocked!")
            if currenttierend != 1:
                newtierlistarray = []
                for x in commandarray_all_valid:
                    newtiereval = eval("tierunlock"+x)
                    if newtiereval == currenttierend:
                        newtierlistarray.append(x)
                if newtierlistarray != []:
                    newtierlist = get_trigger_arg(newtierlistarray, "list")
                    tierchangemsg = str(tierchangemsg + " Feature(s) now available: " + newtierlist)
                combattextarraycomplete.append(tierchangemsg)

        ## Magic Attributes text
        if instigator != target:
            magicattributestext = get_magic_attributes_text(bot, instigator, target, instigatorshieldstart, targetshieldstart, instigatorcursestart, targetcursestart)
            if magicattributestext and magicattributestext != '':
                combattextarraycomplete.append(magicattributestext)
                
        ## Special Event
        speceventtext = ''
        speceventtotal = get_database_value(bot, bot.nick, 'specevent') or 0
        if speceventtotal >= 49:
            set_database_value(bot, bot.nick, 'specevent', 1)
            speceventtext = str(instigator + " triggered the special event! Winnings are "+str(duel_special_event)+" Coins!")
            adjust_database_value(bot, instigator, 'coin', duel_special_event)
            combattextarraycomplete.append(speceventtext)
        else:
            adjust_database_value(bot, bot.nick, 'specevent', 1)

        ## Streaks Text
        streaktext = ''
        if instigator != target:
            streaktext = get_streaktext(bot, winner, loser, winner_loss_streak, loser_win_streak) or ''
            if streaktext != '':
                combattextarraycomplete.append(streaktext)

        ## On Screen Text
        texttargetarray = []
        if OSDTYPE == 'say':
            texttargetarray.append(channel)
        elif OSDTYPE == 'notice':
            texttargetarray.append(instigator)
            texttargetarray.append(target)
        else:
            texttargetarray.append(instigator)
        onscreentext(bot, texttargetarray, combattextarraycomplete)
        
        ## update assault stats
        if winner == instigator:
            assault_wins = assault_wins + 1
            assault_damagedealt = assault_damagedealt + int(damage)
            assault_xp = assault_xp + XPearnedwinner
            if yourclasswinner == 'vampire':
                assault_damagetaken = assault_damagetaken - int(damage)
        if loser == instigator:
            assault_losses = assault_losses + 1
            assault_damagetaken = assault_damagetaken + int(damage)
            assault_xp = assault_xp + XPearnedloser

        ## Pause Between duels
        if typeofduel == 'assault':
            bot.notice("  ", instigator)
            time.sleep(5)
        
        ## Random Bonus
        if typeofduel == 'random' and winner == instigator:
            adjust_database_value(bot, winner, 'coin', random_payout)
            
        ## End Of assault
        if typeofduel == 'assault':
            set_database_value(bot, target, 'lastfought', targetlastfoughtstart)
            if targetarraytotal == 0:
                bot.notice(instigator + ", It looks like the Full Channel Assault has completed.", instigator)
                
                for x in assaultstatsarray:
                    workingvar = eval("assault_"+x)
                    if workingvar > 0:
                        newline = str(x + " = " + str(workingvar))
                        if assaultdisplay != '':
                            assaultdisplay = str(assaultdisplay + " " + newline)
                        else:
                            assaultdisplay = str(newline)
                ##onscreentext(bot, [inchannel], dispmsgarray) TODO: make the assualt stats an array
                bot.say(instigator + "'s Full Channel Assault results: " + assaultdisplay)
