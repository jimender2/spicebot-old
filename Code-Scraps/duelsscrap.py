
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

def damagedone(bot, winner, loser, instigator, weapon, diaglevel, assault_kills, assault_deaths):

    damagetextarray = []
    damagescale = tierratio_level(bot)
    winnerclass = get_database_value(bot, winner, 'class') or 'notclassy'
    loserclass = get_database_value(bot, loser, 'class') or 'notclassy'
    shieldloser = get_database_value(bot, loser, 'shield') or 0
    shieldwinner = get_database_value(bot, winner, 'shield') or 0
    damagetext = ''
    
    ## names
    if winner == 'duelsroulettegame':
        winnername = loser
        losername = "themself"
        striketype = "shoots"
        bodypart = "head"
    elif winnerclass == 'knight' and diaglevel == 2:
        winnername = winner
        losername = loser
        striketype = "retaliates against"
        bodypart = get_trigger_arg(bodypartsarray, 'random')
    elif winner == loser:
        winnername = loser
        losername = "themself"
        striketype = get_trigger_arg(duel_hit_types, 'random')
        bodypart = get_trigger_arg(bodypartsarray, 'random')
    else:
        winnername = winner
        losername = loser
        striketype = get_trigger_arg(duel_hit_types, 'random')
        bodypart = get_trigger_arg(bodypartsarray, 'random')

    ## Armortype to check
    armortype = eval("armor"+bodypart)
    
    ## Rogue can't be hurt by themselves or bot
    roguearraynodamage = [bot.nick,loser]
    if loserclass == 'rogue' and winner in roguearraynodamage:
        damage = 0
    
    elif winner == 'duelsroulettegame':
        damage = randint(50, 120)
    
    ## Bot deals a set amount
    elif winner == bot.nick:
        damage = bot_damage

    ## Barbarians get extra damage (minimum)
    elif winnerclass == 'barbarian':
        damage = randint(duel_advantage_barbarian_min_damage, 120)
    
    ## vampires have a minimum damage
    elif winnerclass == 'vampire' and winner != loser:
        damage = randint(0, duel_disadvantage_vampire_max_damage)
    
    ## All Other Players
    else:
        damage = randint(0, 120)
       
    ## Damage Tiers
    if damage > 0:
        damage = damagescale * damage
        damage = int(damage)

    if damage == 0:
        damagetext = str(winnername + " " + striketype + " " + losername + " in the " + bodypart + weapon + ', but deals no damage. ')
    elif winnerclass == 'vampire' and winner != loser:
        damagetext = str(winnername + " drains " + str(damage)+ " health from " + losername + weapon + " in the " + bodypart + ". ")
    else:
        damagetext = str(winnername + " " + striketype + " " + losername + " in the " + bodypart + weapon + ", dealing " + str(damage) + " damage. ")
    damagetextarray.append(damagetext)
    
    ## Vampires gain health from wins
    if winnerclass == 'vampire' and winner != loser:
        adjust_database_value(bot, winner, 'health', damage)
        
    ## Berserker Rage
    if winnerclass == 'barbarian' and winner != loser:
        rageodds = randint(1, duel_advantage_barbarian_rage_chance)
        if rageodds == 1:
            extradamage = randint(1, duel_advantage_barbarian_rage_max)
            damagetext = str(winner + " goes into Berserker Rage for an extra " + str(extradamage) + " damage.")
            damage = damage + extradamage
            damagetextarray.append(damagetext)
    
    ## Paladin deflect
    if loserclass == 'paladin' and damage > 0 and winner != 'duelsroulettegame' and winner != loser:
        deflectodds = randint(1, duel_advantage_paladin_deflect_chance)
        if deflectodds == 1:
            damageb = damage
            damage = 0
            damagetext = str(damagetext + " "+ loser + " deflects the damage back on " + winner + ". ")
            damagemathb = int(shieldwinner) - damageb
            if int(damagemathb) > 0:
                adjust_database_value(bot, winner, 'shield', -abs(damageb))
                damageb = 0
                absorbedb = 'all'
            else:
                absorbedb = damagemathb + damageb
                damage = abs(damagemathb)
                reset_database_value(bot, loser, 'shield')
            damagetext = str(winner + " absorbs " + str(absorbedb) + " of the damage. ")
            damagetextarray.append(damagetext)

    ## Shield resistance
    if shieldloser and damage > 0 and winner != loser:
        damagemath = int(shieldloser) - damage
        if int(damagemath) > 0:
            adjust_database_value(bot, loser, 'shield', -abs(damage))
            damage = 0
            absorbed = 'all'
        else:
            absorbed = damagemath + damage
            damage = abs(damagemath)
            reset_database_value(bot, loser, 'shield')
        damagetext = str(loser + " absorbs " + str(absorbed) + " of the damage. ")
        damagetextarray.append(damagetext)

    ## Armor usage
    armorloser = get_database_value(bot, loser, armortype) or 0
    if armorloser and damage > 0 and winner != loser:
        adjust_database_value(bot, loser, armortype, -1)
        damagepercent = randint(1, armor_relief_percentage) / 100
        damagereduced = damage * damagepercent
        damagereduced = int(damagereduced)
        damage = damage - damagereduced
        damagetext = str(loser + "s "+ armortype + " aleviated "+str(damagereduced)+" of the damage ")
        armorloser = get_database_value(bot, loser, armortype) or 0
        if armorloser <= 0:
            reset_database_value(bot, loser, armortype)
            damagetext = str(damagetext + ", causing the armor to break!")
        elif armorloser <= 5:
            damagetext = str(damagetext + ", causing the armor to be in need of repair!")
        else:
            damagetext = str(damagetext + ".")
        damagetextarray.append(damagetext)
    
    ## dish it out
    if damage > 0:
        adjust_database_value(bot, loser, 'health', -abs(damage))
    
    ## Update Health Of Loser, respawn, allow winner to loot
    deathmsgb = ''
    losercurrenthealth = get_database_value(bot, loser, 'health')
    if losercurrenthealth <= 0:
        if winner == loser:
            deathmsgb = suicidekill(bot,loser)
        else:
            deathmsgb = whokilledwhom(bot, winner, loser) or ''
        winnermsg = str(loser + ' dies forcing a respawn!!')
        damagetextarray.append(winnermsg)
        if winner != loser:
            if winner == instigator:
                assault_kills = assault_kills + 1
            else:
                assault_deaths = assault_deaths + 1
        if deathmsgb != '':
            damagetextarray.append(deathmsgb)
    
    ## Knight
    if loserclass == 'knight' and diaglevel != 2 and winner != 'duelsroulettegame' and winner != loser:
        retaliateodds = randint(1, duel_advantage_knight_retaliate_chance)
        if retaliateodds == 1:
            weaponb = weaponofchoice(bot, loser)
            weaponb = weaponformatter(bot, weaponb)
            weaponb = str(" "+ weaponb)
            damage, damagetextb, assault_kills, assault_deaths = damagedone(bot, loser, winner, instigator, weaponb, 2, assault_kills, assault_deaths)
            #damageb, damagetextb = damagedone(bot, loser, winner, weaponb, 2)
            for x in damagetextb:
                damagetextarray.append(x)
    
    return damage, damagetextarray, assault_kills, assault_deaths
